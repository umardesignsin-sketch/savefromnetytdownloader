import { DurableObject } from 'cloudflare:workers';

const DAY = 86_400_000;
const LIVE_WINDOW = 5 * 60_000;

export class VisitorAnalytics extends DurableObject {
  constructor(ctx, env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    this.sql.exec(`CREATE TABLE IF NOT EXISTS visitors (
      day TEXT NOT NULL,
      visitor TEXT NOT NULL,
      country TEXT NOT NULL,
      first_seen INTEGER NOT NULL,
      last_seen INTEGER NOT NULL,
      page_views INTEGER NOT NULL DEFAULT 0,
      PRIMARY KEY (day, visitor)
    )`);
    this.sql.exec('CREATE INDEX IF NOT EXISTS visitors_last_seen ON visitors(last_seen)');
  }

  async fetch(request) {
    const path = new URL(request.url).pathname;
    const now = Date.now();
    const day = new Date(now).toISOString().slice(0, 10);
    if (path === '/visit' && request.method === 'POST') {
      const { visitor, country, kind } = await request.json();
      if (!/^[a-f0-9]{64}$/.test(visitor) || !/^[A-Z]{2}$/.test(country) ||
          !['page', 'heartbeat'].includes(kind)) return new Response('Invalid visit', { status: 400 });
      this.sql.exec(`INSERT INTO visitors (day, visitor, country, first_seen, last_seen, page_views)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(day, visitor) DO UPDATE SET
          country = excluded.country, last_seen = excluded.last_seen,
          page_views = visitors.page_views + excluded.page_views`,
      day, visitor, country, now, now, kind === 'page' ? 1 : 0);
      if (!await this.ctx.storage.getAlarm()) await this.ctx.storage.setAlarm(now + DAY);
      return new Response(null, { status: 204 });
    }
    if (path === '/stats' && request.method === 'GET') {
      const liveSince = now - LIVE_WINDOW;
      const summary = this.sql.exec(`SELECT COUNT(*) AS visitors,
        COALESCE(SUM(page_views), 0) AS pageViews,
        SUM(CASE WHEN last_seen >= ? THEN 1 ELSE 0 END) AS live
        FROM visitors WHERE day = ?`, liveSince, day).one();
      const countries = this.sql.exec(`SELECT country, COUNT(*) AS visitors,
        SUM(CASE WHEN last_seen >= ? THEN 1 ELSE 0 END) AS live
        FROM visitors WHERE day = ? GROUP BY country ORDER BY visitors DESC`, liveSince, day).toArray();
      const hours = this.sql.exec(`SELECT CAST(strftime('%H', first_seen / 1000, 'unixepoch') AS INTEGER) AS hour,
        COUNT(*) AS visitors FROM visitors WHERE day = ? GROUP BY hour ORDER BY hour`, day).toArray();
      return Response.json({
        day, generatedAt: new Date(now).toISOString(), liveWindowMinutes: 5,
        visitorsToday: summary.visitors || 0, liveVisitors: summary.live || 0,
        pageViewsToday: summary.pageViews || 0,
        countries: countries.map(row => ({ country: row.country, visitors: row.visitors, live: row.live || 0 })),
        hours,
      }, { headers: { 'Cache-Control': 'no-store' } });
    }
    return new Response('Not found', { status: 404 });
  }

  async alarm() {
    this.sql.exec('DELETE FROM visitors WHERE last_seen < ?', Date.now() - 2 * DAY);
    if (this.sql.exec('SELECT COUNT(*) AS n FROM visitors').one().n > 0) {
      await this.ctx.storage.setAlarm(Date.now() + DAY);
    }
  }
}
