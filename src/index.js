import 'leaflet/dist/leaflet.css';
import './style.css';

let L = require('leaflet');
// require('leaflet-routing-machine');

let map = L.map('map').setView([0, 0], 0);

const localTileServer = 'http://0.0.0.0:8080/tile/{z}/{x}/{y}.png'
const leafletTileServer = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

L.tileLayer(
  leafletTileServer, 
  { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }
).addTo(map);

map.locate({setView: true})
  .on("locationfound", (e) => {
    console.log(e);
  });

