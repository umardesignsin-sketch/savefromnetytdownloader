// Natural Earth 1:110m countries are public domain: https://www.naturalearthdata.com/about/terms-of-use/
// Run with a downloaded ne_110m_admin_0_countries.geojson to refresh the globe geometry.
import { readFileSync, writeFileSync } from 'node:fs';

const source = JSON.parse(readFileSync(process.argv[2], 'utf8'));
function simplify(points) {
  if (points.length < 8) return points.map(([lon, lat]) => [Math.round(lon * 10) / 10, Math.round(lat * 10) / 10]);
  const output = [];
  for (let i = 0; i < points.length; i += 3) {
    const [lon, lat] = points[i];
    output.push([Math.round(lon * 10) / 10, Math.round(lat * 10) / 10]);
  }
  return output.length >= 3 ? output : points.slice(0, 3);
}
const countries = source.features.flatMap(feature => {
  const p = feature.properties;
  const code = p.ISO_A2_EH || p.ISO_A2;
  if (!/^[A-Z]{2}$/.test(code)) return [];
  const polygons = feature.geometry.type === 'Polygon' ? [feature.geometry.coordinates] : feature.geometry.coordinates;
  return [{
    code, name: p.NAME_EN || p.NAME, lat: p.LABEL_Y, lon: p.LABEL_X,
    rings: polygons.flatMap(polygon => polygon.slice(0, 1)).map(simplify).filter(ring => ring.length >= 3),
  }];
});
writeFileSync(new URL('../src/analytics-world.json', import.meta.url), JSON.stringify(countries));
console.log(`Saved ${countries.length} countries`);
