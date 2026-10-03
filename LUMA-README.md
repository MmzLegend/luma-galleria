# LUMA GALLERIA

An original architectural mall concept inspired by the circulation and program of the supplied floor plan. It is a new design with chosen dimensions, rather than a dimensionally verified reconstruction of that image.

## Explore

The connected Mac viewer is at **http://127.0.0.1:8895**. Refresh an existing viewer tab to see the new concept.

To run the portable package elsewhere, unzip it, open a terminal in its folder and run `sh run.sh`. The viewer and included Three.js dependency work locally without a network connection. Port 8895 must be available. No production deployment or external hosting is involved.

Use Exterior, Arrival, Atrium, Cutaway and Top presets; drag to orbit, scroll to zoom and right-drag to pan. Roof/skylights, exterior shell, landscape/furniture and plan labels can be toggled. Click a shop floor or storefront for its concept bounds and area. The floor plan opens in a dialog and is also available as editable SVG and PNG.

## The design

The building has a **74 × 100 m** footprint and one occupied public level. Sixteen retail units and two dining restaurants flank an **18 m wide central atrium**, a **12 m cross gallery** and two **5 m secondary galleries**. Four guest/management rooms complete the 22-unit program. The north dining lounge opens onto restaurant terraces; the south foyer opens onto a landscaped arrival plaza.

The material system combines warm limestone, bronze frames, charcoal storefront fascia, timber shop floors/fixtures, terrazzo public circulation and blue-green glazing. The central atrium has a gabled glazed roof: **6.2 m eaves** and **9.0 m nominal ridge**, with real roof panels, purlins, rafters, ties and columns. Cross-gallery skylights and secondary daylight ribbons meet opaque metal roofs over the shops. Parapets, glazing upstands and gable glazing complete the shell. Rooftop photovoltaic modules are modeled as a design feature; no energy performance is claimed.

The entrance includes a glass curtain wall, bronze canopy, limestone piers and embossed 3D lettering. Shopfronts include transparent panes, sliding-door leaves, pulls, mullions, transoms, fascia and dimensional names. Internal fit-outs include shelf products, display tables, dining furniture, restroom fittings, lounge seating, benches, trees, a reflecting-water court and bronze sculpture. The site includes forecourt paving/joints, raised planting, bollards, side paths, perimeter trees, terrace furniture and parasols.

Two lift enclosures mark vertical circulation provision; levels served are not modeled or engineered. A 28-tread maintenance stair rises to a modeled roof access hatch. There is no invented occupied upper level.

## Editable files

- **`luma-galleria.glb`** — complete real glTF 2.0 binary scene, editable in Blender and other glTF editors. Materials, transparent glazing, named scene objects, roof categories and embossed text are included in the model itself.
- **`build_luma.py`** — editable standard-library Python source for the architecture, unit bounds, fittings, site, raw GLB and vector plan. Dimensions are explicit metres.
- **`export_luma.mjs`** — adds real extruded lettering and writes the final GLB. Uses the included Three.js dependency and official Helvetiker font asset.
- **`luma-layout.json`** — readable shared layout, rooms, storefronts, text placements, object transforms and material names.
- **`luma-floorplan.svg` / `luma-floorplan.png`** — matching dimensioned ground-floor plan, generated from the same unit bounds and storefront coordinates as the model. Area figures represent concept room rectangles, not surveyed net lettable areas.
- **`index.html` / `luma-viewer.js` / `run.sh`** — local interactive viewer.
- **`luma-renders/`** — real model renders: exterior, atrium interior, cutaway, top, labelled top and complete viewer.
- **`luma-validation.json`, `luma-export-validation.json`, `luma-browser-validation.json`** — generation, exported bounds and actual browser checks.

Regenerate with:

```sh
python3 build_luma.py
node export_luma.mjs
```

The viewer uses vendored MIT-licensed Three.js. Run `npm ci` before rebuilding the GLB with the Node exporter. The PNG plan and PNG views are verified browser captures; the SVG plan regenerates directly from Python. The concept was checked using an isolated browser: model bounds, glass materials, roof toggles, camera presets and matching plan.

## Units, origin and orientation

One GLB unit is one metre. The southwest building corner is **X = 0, Y = 0, Z = 0**; X increases east, Y up, and negative Z north. The footprint spans X 0–74 and Z -100–0. The source layout uses positive northing for convenient plan coordinates; the export explicitly reflects northing into negative Z and regenerates lettering with the correct orientation. That transform is retained on the named architecture parent, so the source is editable and all normals/materials remain supported by glTF viewers. Top view agrees with the SVG orientation: north up, east right.

The complete site spans 110 × 144 m. Its geometry contributes to model bounds; it should not be mistaken for building footprint dimensions. The roof cap extends slightly beyond the nominal ridge height.

## Verification and limitations

The actual exported GLB was loaded into the viewer and its bounds/materials inspected. Roof visibility was tested off and restored; shell and furniture toggles, all camera presets, plan dialog and reset were exercised. Transparent storefront and roof materials render as transparent, with non-shadow-casting glass allowing daylight into the atrium. Roof and interior scenes were visually inspected, and the rendered top view compared against the matching SVG plan. The room rectangles and floor meshes are generated from the same data.

This is an architectural concept visualization. Structure, foundations, fire strategy, accessibility, mechanical/electrical systems, service/loading logistics, lift operation and roof access details are not engineered. Wall and roof thicknesses, materials, fittings, shop identities and all dimensions are design choices. It is not certified construction documentation.


Dependency: Three.js (MIT license included). Font asset: official Three.js Helvetiker example, retained as `assets/helvetiker_regular.typeface.json` with its embedded provenance.