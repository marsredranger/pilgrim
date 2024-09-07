import 'leaflet/dist/leaflet.css';
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css'
import './style.css';
import redPin from './pin-red-icon-32.png';
import greenPin from './pin-green-icon-32.png';
import pinShadow from './pin-shadow-32.png';
let L = require('leaflet');
require('leaflet-routing-machine');

let createImage = function(src) {
  let image = new Image();
  image.src = src;
  return image;
}

let createIcon = function(pinImage, shadowImage) {
  return L.icon({
    iconUrl: pinImage.src, 
    iconSize: [pinImage.width, pinImage.height], 
    iconAnchor: [pinImage.width/2, pinImage.height],
    shadowUrl: shadowImage.src,
    shadowSize: [shadowImage.width, shadowImage.height],
    shadowAnchor: [16, 30]
  });
}

let map = L.map('map').setView([0, 0], 0);
const localTileServer = 'http://0.0.0.0:8080/tile/{z}/{x}/{y}.png'
const leafletTileServer = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'

const routingServiceUrl = 'http://0.0.0.0:5050/route/v1';
L.tileLayer(
  leafletTileServer, 
  { attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' }
).addTo(map);

let redPinImage = createImage(redPin); 
let pinShadowImage = createImage(pinShadow);
let greenPinImage = createImage(greenPin);
let redPinIcon = createIcon(redPinImage, pinShadowImage); 
let greenPinIcon = createIcon(greenPinImage, pinShadowImage) 

let origin;
let destination;
let route;

map.on('click', function(e) {
  if(!origin && !destination) {
    origin = L.marker([e.latlng.lat, e.latlng.lng], {icon: greenPinIcon}).addTo(map);
  } else {
    if (destination) {
      destination.remove();
      route.remove();
    }
    destination = L.marker([e.latlng.lat, e.latlng.lng], {icon: redPinIcon}).addTo(map);
    route = L.Routing.control({
      waypoints: [origin.getLatLng(), destination.getLatLng()],
      createMarker: function(i, waypoint, n) {
        return i === 0 ? origin : destination
      },
      serviceUrl: routingServiceUrl,
    }).addTo(map)
  }
})
