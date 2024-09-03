import { VectorTile } from "@mapbox/vector-tile";
import Protobuf from "pbf";
import fs from "fs";

const tile = new VectorTile(new Protobuf(fs.readFileSync("90.mvt")));

// Contains a map of all layers
console.log(tile.layers.pois);

console.log(new Protobuf(tile.layers.pois._pbf));

const landuse = tile.layers.landuse;

// Amount of features in this layer
// console.log(landuse.length);

// Returns the first feature
// console.log(landuse.feature(0));
