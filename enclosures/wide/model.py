"""Wide transmitter enclosure: Heltec Wireless Stick Lite V3 + protected 18650 cell.

Parametric FreeCAD (Part) model. Runs in the FreeCAD GUI or in freecadcmd. Dimensions in
mm; origin at the outer bottom corner of the body, x along the length, y across the
width, z up.

Installed upright, with the back (z = 0) against a wall: the -X face points down, with the
USB-C opening and the cable gland, so splashes do not get in; the +X face points up, with
the antenna. Lid and board carrier are held by M3 screws in heat-set inserts: no hole goes
through the back, which stays closed and flat against the wall.

Values marked as estimates must be measured on the actual parts before relying on them.
"""

import FreeCAD as App
import Part
from FreeCAD import Vector as V

P = {
    # Walls and closure
    "wall": 2.4,
    "floor": 2.4,
    "lid": 2.4,
    "corner_radius": 3.0,
    # Usable inner space
    # Length +10 mm and height +2 mm in r04: on the r03 print the cable gland touched the
    # battery and there was no room to route the cables above it
    "inner_length": 103.0,
    "inner_width": 55.0,
    "inner_height": 25.0,
    # Cylindrical cell, measured
    "battery_length": 66.40,
    "battery_diameter": 18.53,
    "battery_radial_clearance": 0.4,
    # Free space at the bottom end (-X): inner side of the cable gland and the bend of the
    # sensor cable towards the board band. With 14 mm the battery touched the gland; with
    # 24 mm about 17 mm remain between the end of the thread and the stop. The battery
    # terminals sit at the top end: the cable enters the board connector next to the USB,
    # runs under the board and leaves at the opposite end
    "bottom_space": 24.0,
    # Stop at the bottom end of the battery: with the enclosure upright, the battery slid
    # down to the cable gland
    "battery_stop_thickness": 1.6,
    "battery_stop_height": 8.0,
    "battery_floor_clearance": 1.2,
    # Wireless Stick Lite V3, datasheet Rev1.1 section 4.1
    "board_length": 58.08,
    "board_width": 22.6,
    "board_total_height": 8.2,
    "board_thickness": 1.6,
    # Only the battery connector sits under the board, 3.4 mm (measured); USB-C and module
    # are on top. USB-C height and how far it overhangs the edge: estimates
    "board_bottom_components": 3.4,
    # 2.6 mm under the connector so the battery cable runs under the board without being
    # pinched (0.6 mm before r03)
    "board_clearance_below_components": 2.6,
    "board_usb_overhang": 1.0,
    "board_usb_center_above_pcb": 1.6,
    "board_usb_wall_clearance": 0.5,
    # RST and USER side buttons, at the corners of the USB end, protruding from the long
    # edges. The datasheet gives no button dimensions: position, protrusion and height are
    # estimated from the drawing scale (TODO: measure with calipers)
    "board_button_start": 0.9,
    "board_button_length": 3.4,
    "board_button_protrusion": 0.8,
    "board_button_height": 3.5,
    # Separate carrier with rails: the board slides in from the USB end outside the
    # enclosure, up to the heads, and the carrier drops onto the floor pins. Side clearance
    # and slot carried over from an earlier carrier that held the board well
    "rail_width": 2.0,
    "rail_capture": 0.6,
    "rail_side_clearance": 0.175,
    "rail_slot": 2.2,
    "rail_lip": 1.6,
    # Rails start after the SH1.25 connectors, at the corners of the USB end
    "rail_start": 7.0,
    # Crossbars under the board at both ends of the rails: without them the rails spread
    # and released the board (r01). The middle stays open for airflow and for the battery
    # cable. In bending, two 10 x 1.6 mm crossbars add up to about the same as the solid
    # 1.2 mm base of r02 (width x thickness³). 4.4 mm remain above the crossbars and 6 mm
    # in the open middle
    "carrier_base": 1.6,
    "carrier_crossbar": 10.0,
    # Screwless carrier fit: two square heads at the end of the rails, flush with their
    # outer face, drop onto two floor pins that hold the carrier in plane. When closed, two
    # lid posts stop 0.3 mm above the heads, so the carrier cannot leave the pins. 8.6 mm
    # stay free between the heads for the battery cable adapter, which is as long as the
    # board (2.8 mm in r02, where it barely passed)
    "pin_diameter": 5.0,
    "pin_height": 6.0,
    "pin_chamfer": 0.8,
    "pin_clearance": 0.2,
    "head_side": 9.0,
    "lid_post_side": 6.0,
    "lid_post_clearance": 0.3,
    # Openings
    "usb_opening_width": 12.5,
    "usb_opening_height": 7.0,
    "antenna_hole": 6.8,  # bulkhead SMA
    "gland_hole": 8.4,  # M8x1.25, 2 to 4 mm cable
    # Inner part of the cable gland, for clearance checks only: 7.5 mm thread (supplier
    # table) minus the wall; nut enclosed by a cylinder (TODO: measure the actual nut)
    "gland_inner_thread": 5.1,
    "gland_nut_diameter": 14.0,
    "gland_nut_thickness": 4.0,
    # USB-C opening cover: friction fit, not reaching past the wall, because the connector
    # sits 0.5 mm behind it
    "usb_cover_width_clearance": 0.1,
    "usb_cover_height_clearance": 0.15,
    "usb_cover_depth": 2.2,
    "usb_cover_flange": 2.5,
    "usb_cover_thickness": 1.6,
    # Closure: columns in the inner corners with a heat-set insert at the top; lid held by
    # M3x8 (2.4 mm of lid + 5.6 mm inside the insert)
    "column_side": 7.0,
    "m3_hole": 3.4,
    # Hole for an M3 insert 5.7 mm long and Ø4.6 outside, with 0.8 mm spare at the bottom
    # for displaced plastic (TODO: check against the insert actually used)
    "insert_hole": 4.0,
    "insert_depth": 6.5,
    # 45° chamfer at the mouth of the hole, from Ø4.0 to Ø5.0, so the insert starts centred
    # and upright: in r04, without it, inserts set with a soldering iron ended up off
    # centre. It also takes the plastic that rises around the insert. With 0 the hole is
    # the r04 one
    "insert_chamfer": 0.5,
    "tab_width": 12.0,
    "tab_reach": 9.0,
    "tab_thickness": 3.0,
    "tab_hole": 4.5,
    "lip_width": 1.2,
    "lip_height": 3.0,
}


def box(x, y, z, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x, y, z))


def cylinder(r, h, base, direction):
    return Part.makeCylinder(r, h, base, direction)


def round_vertical_edges(shape, radius):
    edges = [
        e
        for e in shape.Edges
        if abs(e.Vertexes[0].Point.x - e.Vertexes[-1].Point.x) < 1e-6
        and abs(e.Vertexes[0].Point.y - e.Vertexes[-1].Point.y) < 1e-6
    ]
    return shape.makeFillet(radius, edges)


def geometry(p=P):
    t, fl = p["wall"], p["floor"]
    lin, win, hin = p["inner_length"], p["inner_width"], p["inner_height"]
    L, W, hb = lin + 2 * t, win + 2 * t, fl + hin
    ins_r, ins_depth = p["insert_hole"] / 2, p["insert_depth"]

    # Battery: band along -Y, wires at the -X end
    db, lb = p["battery_diameter"], p["battery_length"]
    xb0 = t + p["bottom_space"]
    yb = t + 1.0 + db / 2
    zb = fl + p["battery_floor_clearance"] + db / 2
    battery_band = t + 1.0 + db + 1.0

    # Board: band along +Y, USB-C at the -X wall
    lp, wp = p["board_length"], p["board_width"]
    divider = 1.6
    y_board_band = battery_band + divider + 0.3
    yp0 = y_board_band + p["rail_width"]
    xp0 = t + p["board_usb_wall_clearance"] + p["board_usb_overhang"]
    zp = fl + p["board_bottom_components"] + p["board_clearance_below_components"]

    body = round_vertical_edges(box(0, 0, 0, L, W, hb), p["corner_radius"])
    cavity = round_vertical_edges(box(t, t, fl, lin, win, hin + 1), 1.0)
    body = body.cut(cavity)

    # Battery cradles: two supports with a cylindrical seat
    for xc in (xb0 + 10, xb0 + lb - 16):
        cradle = box(xc, t, fl, 6, battery_band - t, zb - fl)
        cradle = cradle.cut(
            cylinder(db / 2 + p["battery_radial_clearance"], 8, V(xc - 1, yb, zb), V(1, 0, 0))
        )
        body = body.fuse(cradle)

    # Stop at the bottom end of the battery, below the cable gland, so the sensor cable
    # passes over it
    x_stop = xb0 - 0.5 - p["battery_stop_thickness"]
    body = body.fuse(
        box(x_stop, t, fl, p["battery_stop_thickness"], battery_band - t, p["battery_stop_height"])
    )

    # Low divider between battery and board, from the stop to the end of the board: before
    # it the sensor cable crosses to the board band; after it the battery cable and the
    # adapter cross to the terminals, at the top end
    x_board_end = t + p["board_usb_wall_clearance"] + p["board_usb_overhang"] + p["board_length"]
    body = body.fuse(box(x_stop, battery_band, fl, x_board_end - x_stop, divider, 10))

    # Board carrier (separate part), printed with the crossbars on the bed: crossbars at the
    # ends joining the rails, rails with a slot closed at the top end and two heads that
    # drop onto the floor pins. Between the heads the path is open from the floor up, for
    # the battery cable and the adapter
    rail_w, cap, clr = p["rail_width"], p["rail_capture"], p["rail_side_clearance"]
    slot, lip_r, ep = p["rail_slot"], p["rail_lip"], p["board_thickness"]
    z_slot = zp - (slot - ep) / 2
    z_top = z_slot + slot + lip_r
    x_start, x_end = xp0 + p["rail_start"], xp0 + lp
    y_out0, y_out1 = yp0 - rail_w, yp0 + wp + rail_w
    base, bar, head = p["carrier_base"], p["carrier_crossbar"], p["head_side"]
    # The heads start at the end of the slot and act as the board stop
    x_head = x_end + 0.2
    pins = [(x_head + head / 2, y_out0 + head / 2), (x_head + head / 2, y_out1 - head / 2)]
    # Top crossbar and rails reach 1 mm into the heads so they fuse into one part
    carrier = box(x_start, y_out0, fl, bar, y_out1 - y_out0, base).fuse(
        box(x_end - bar, y_out0, fl, bar + 1.2, y_out1 - y_out0, base)
    )
    for edge, sign in ((yp0, -1), (yp0 + wp, 1)):
        y_rail = edge - rail_w if sign < 0 else edge - cap
        rail = box(x_start, y_rail, fl, x_head + 1 - x_start, rail_w + cap, z_top - fl)
        y_slot = edge - clr - 0.4 if sign < 0 else edge - cap - 1
        rail = rail.cut(box(x_start - 1, y_slot, z_slot, x_head - x_start + 1, cap + clr + 1.4, slot))
        carrier = carrier.fuse(rail)
    r_pin = p["pin_diameter"] / 2
    for px, py in pins:
        head_block = box(x_head, py - head / 2, fl, head, head, z_top - fl)
        outer_corners = [e for e in head_block.Edges if e.Vertexes[0].Point.x > x_head + head - 1e-6
                         and abs(e.Vertexes[0].Point.z - e.Vertexes[-1].Point.z) > 1e-6]
        carrier = carrier.fuse(head_block.makeFillet(1.5, outer_corners))
    for px, py in pins:
        # Blind pin socket: the top of the head stays flat, where the lid post rests
        carrier = carrier.cut(
            cylinder(r_pin + p["pin_clearance"], p["pin_height"] + 0.4, V(px, py, fl - 0.1), V(0, 0, 1))
        )
        ch = p["pin_chamfer"]
        body = body.fuse(cylinder(r_pin, p["pin_height"] - ch, V(px, py, fl), V(0, 0, 1)))
        body = body.fuse(Part.makeCone(r_pin, r_pin - ch, ch, V(px, py, fl + p["pin_height"] - ch)))

    # USB-C opening in the -X wall; the connector sits on top of the board
    yc_board = yp0 + wp / 2
    zc_usb = zp + ep + p["board_usb_center_above_pcb"]
    body = body.cut(
        box(
            -1,
            yc_board - p["usb_opening_width"] / 2,
            zc_usb - p["usb_opening_height"] / 2,
            t + 2,
            p["usb_opening_width"],
            p["usb_opening_height"],
        )
    )
    # USB-C cover, drawn with the flange on the bed (XY plane) and moved into the assembly:
    # flange outside the wall, plug inside the opening and a pull tab facing the front of
    # the enclosure (+Z), away from the wall it is mounted on
    flange_w = p["usb_opening_width"] + 2 * p["usb_cover_flange"]
    flange_h = p["usb_opening_height"] + 2 * p["usb_cover_flange"]
    e_flange = p["usb_cover_thickness"]
    usb_cover = round_vertical_edges(box(-flange_w / 2, -flange_h / 2, 0, flange_w, flange_h, e_flange), 2.0)
    usb_cover = usb_cover.fuse(box(-3, flange_h / 2 - 1, 0, 6, 4, e_flange))
    usb_cover = usb_cover.fuse(cylinder(3, e_flange, V(0, flange_h / 2 + 3, 0), V(0, 0, 1)))
    plug_w = p["usb_opening_width"] - 2 * p["usb_cover_width_clearance"]
    plug_h = p["usb_opening_height"] - 2 * p["usb_cover_height_clearance"]
    usb_cover = usb_cover.fuse(
        box(-plug_w / 2, -plug_h / 2, e_flange, plug_w, plug_h, p["usb_cover_depth"])
    )
    # Local (x, y, z) -> assembly (y, z, x): width along Y, height along Z, plug along +X
    usb_cover = usb_cover.transformGeometry(App.Matrix(0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1))
    usb_cover.translate(V(-e_flange, yc_board, zc_usb))

    # Sensor cable gland at the bottom (-X), in the battery band, away from the corner column
    y_gland, z_gland = yb + 5, fl + 12
    body = body.cut(cylinder(p["gland_hole"] / 2, t + 2, V(-1, y_gland, z_gland), V(1, 0, 0)))
    # SMA antenna at the top (+X), in line with the board band
    body = body.cut(cylinder(p["antenna_hole"] / 2, t + 2, V(L - t - 1, yc_board, fl + 13), V(1, 0, 0)))

    # Columns in the inner corners, joined to the walls, with an insert from the top for the lid
    c = p["column_side"]
    corners = [(t, t), (L - t - c, t), (t, W - t - c), (L - t - c, W - t - c)]
    centres = [(x + c / 2 - (0.6 if x == t else -0.6), y + c / 2 - (0.6 if y == t else -0.6)) for x, y in corners]
    # The (+Y, -X) column only fills the upper half: full height, it pressed the USER button
    # (r03 print). Underneath, a 45° chamfer from both walls lets it print without support;
    # the insert hole stays entirely in the upper half
    button_corner = (t, W - t - c)
    for x, y in corners:
        if (x, y) != button_corner:
            body = body.fuse(box(x, y, fl, c, c, hin))
            continue
        z0 = fl + hin / 2
        body = body.fuse(box(x, y, z0, c, c, hb - z0))
        ramp_x = Part.Face(Part.makePolygon([V(t, y, z0 - c), V(t, y, z0), V(t + c, y, z0), V(t, y, z0 - c)]))
        ramp_y = Part.Face(Part.makePolygon([V(x, W - t, z0 - c), V(x, W - t, z0), V(x, y, z0), V(x, W - t, z0 - c)]))
        body = body.fuse(ramp_x.extrude(V(0, c, 0)).common(ramp_y.extrude(V(c, 0, 0))))
    ins_ch = p["insert_chamfer"]
    for cx, cy in centres:
        body = body.cut(cylinder(ins_r, ins_depth + 1, V(cx, cy, hb - ins_depth), V(0, 0, 1)))
        if ins_ch:
            # 45° cone running 1 mm past the top, so the cut leaves no coplanar face
            body = body.cut(Part.makeCone(ins_r, ins_r + ins_ch + 1, ins_ch + 1, V(cx, cy, hb - ins_ch)))

    # Mounting tabs on the sides (±Y), flush with the back: away from USB, gland and antenna
    for ya, sign in ((0, -1), (W, 1)):
        tab = box(
            L / 2 - p["tab_width"] / 2,
            ya if sign > 0 else ya - p["tab_reach"],
            0,
            p["tab_width"],
            p["tab_reach"],
            p["tab_thickness"],
        )
        tab = tab.cut(
            cylinder(p["tab_hole"] / 2, 10, V(L / 2, ya + sign * p["tab_reach"] / 2, -1), V(0, 0, 1))
        )
        body = body.fuse(tab)

    # Flat lid with an inner alignment lip, interrupted at the columns
    tl = p["lid"]
    lid = round_vertical_edges(box(0, 0, hb, L, W, tl), p["corner_radius"])
    lip, lip_h = p["lip_width"], p["lip_height"]
    ring = box(t + 0.3, t + 0.3, hb - lip_h, lin - 0.6, win - 0.6, lip_h).cut(
        box(t + 0.3 + lip, t + 0.3 + lip, hb - lip_h - 1, lin - 0.6 - 2 * lip, win - 0.6 - 2 * lip, lip_h + 2)
    )
    for x, y in corners:
        ring = ring.cut(box(x - 0.3, y - 0.3, hb - lip_h - 1, c + 0.6, c + 0.6, lip_h + 2))
    lid = lid.fuse(ring)
    # Posts that keep the carrier on the pins with the lid closed
    post, z_post = p["lid_post_side"], z_top + p["lid_post_clearance"]
    for px, py in pins:
        lid = lid.fuse(box(px - post / 2, py - post / 2, z_post, post, post, hb - z_post + 0.1))
    for cx, cy in centres:
        lid = lid.cut(cylinder(p["m3_hole"] / 2, tl + 2, V(cx, cy, hb - 1), V(0, 0, 1)))

    # Ghost parts for visual checks (not printed)
    battery = cylinder(db / 2, lb, V(xb0, yb, zb), V(1, 0, 0))
    pcb = box(xp0, yp0, zp, lp, wp, ep)
    below = p["board_bottom_components"]
    above = p["board_total_height"] - ep - below
    connectors = [box(xp0 + 0.5, yy, zp - below, 3.0, 4.3, below) for yy in (yp0 + 0.5, yp0 + wp - 4.8)]
    usb = box(xp0 - p["board_usb_overhang"], yc_board - 4.5, zp + ep, 7.5, 9.0, above)
    module = box(xp0 + 12, yp0 + 3, zp + ep, lp - 24, wp - 6, above * 0.8)
    prot, bt_w = p["board_button_protrusion"], 3.3
    buttons = [
        box(xp0 + p["board_button_start"], y0, zp + ep, p["board_button_length"], bt_w, p["board_button_height"])
        for y0 in (yp0 - prot, yp0 + wp + prot - bt_w)
    ]
    board = pcb.fuse([usb, module] + connectors + buttons)
    gland = cylinder(4.0, t + p["gland_inner_thread"], V(0, y_gland, z_gland), V(1, 0, 0)).fuse(
        cylinder(p["gland_nut_diameter"] / 2, p["gland_nut_thickness"], V(t, y_gland, z_gland), V(1, 0, 0))
    )

    return {
        "Body": body.removeSplitter(),
        "Board_carrier": carrier.removeSplitter(),
        "Lid": lid.removeSplitter(),
        "Usb_cover": usb_cover.removeSplitter(),
        "Ghost_battery": battery,
        "Ghost_board": board,
        "Ghost_gland": gland,
    }, {"outer": (L, W, hb + tl)}


COLORS = {
    "Body": ((0.82, 0.84, 0.80), 0),
    "Lid": ((0.70, 0.76, 0.72), 55),
    "Board_carrier": ((0.85, 0.55, 0.20), 0),
    "Usb_cover": ((0.85, 0.55, 0.20), 0),
    "Ghost_gland": ((0.25, 0.25, 0.25), 0),
    "Ghost_battery": ((0.15, 0.35, 0.75), 0),
    "Ghost_board": ((0.10, 0.45, 0.25), 0),
}


def build(name="WideEnclosure"):
    doc = App.getDocument(name) if name in App.listDocuments() else App.newDocument(name)
    for obj in list(doc.Objects):
        doc.removeObject(obj.Name)
    shapes, dimensions = geometry()
    for obj_name, shape in shapes.items():
        obj = doc.addObject("Part::Feature", obj_name)
        obj.Shape = shape
        if App.GuiUp:
            color, transparency = COLORS[obj_name]
            obj.ViewObject.ShapeColor = color
            obj.ViewObject.Transparency = transparency
    doc.recompute()
    return doc, dimensions
