"""Receiver enclosure for the Heltec WiFi LoRa 32 V3, mains powered.

Parametric FreeCAD (Part) model. Runs in the FreeCAD GUI or in freecadcmd. Dimensions in
mm; origin at the outer bottom corner of the body, x along the length, y across the
width, z up.

Sits flat on a shelf, like a modem: the board lies with the OLED facing up under a window
in the lid, the USB-C leaves through the back wall (-X) and the antenna stands up from the
lid at the back corner. There is no battery. The header pins must be removed from the
board: the model assumes a bare PCB with the OLED as its tallest part. Lid and board
carrier follow the transmitter enclosure: M3 screws in heat-set inserts, a carrier with
rails that drops onto floor pins.

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
    # Usable inner space. Width: 7.5 mm band for the back columns on the -Y side (the board
    # starts 2 mm from the back wall, where a full-height corner column would hit it), the
    # carrier, then a 13 mm band on the +Y side for the antenna pigtail and the SMA
    # connector. Height: the SMA bulkhead body and the bend of the pigtail need about 16 mm
    # under the lid (estimate), so the board is raised on a tall carrier base to keep the
    # OLED close to the window
    "inner_length": 64.0,
    "inner_width": 50.5,
    "inner_height": 18.0,
    # WiFi LoRa 32 V3. Length from the datasheet Rev1.1 section 4.1 (50.2 x 25.5 overall);
    # an earlier caliper reading gave 51.96, which may have included the USB-C. The heads
    # locate the board by its antenna end, so the difference only moves the USB end: the
    # lid openings over the buttons are stretched by it along X to fit either length.
    # Width and thickness measured with calipers
    "board_length": 50.2,
    "board_length_alt": 51.96,
    "board_width": 25.35,
    "board_thickness": 1.63,
    # Battery connector under the board, 3.13 mm (measured); its position is not known,
    # so the clearance applies over the whole carrier, crossbars included
    "board_bottom_components": 3.13,
    "board_clearance_below_components": 1.2,
    # OLED: glass 33.28 x 18.56 mm, centred across the board, 2.4 mm from the antenna end
    # (datasheet drawing scale; a photo suggests it is closer to the end). Top of the
    # glass 5.61 mm above the PCB (measured)
    "oled_length": 33.28,
    "oled_width": 18.56,
    "oled_from_front_end": 2.4,
    "oled_height": 5.61,
    "oled_lid_clearance": 1.0,
    # USB-C on top of the board, 3.0 mm tall (measured). Overhang past the PCB edge is an
    # estimate: it looks flush on the board, the datasheet drawing suggests up to 2.4 mm. A
    # larger value only moves the board away from the wall
    "board_usb_overhang": 1.5,
    "board_usb_height": 3.0,
    "board_usb_width": 9.0,
    "board_usb_wall_clearance": 0.5,
    # RST and PRG tactile switches on top, at the USB end, 2.0 mm tall (measured). Centres
    # estimated from a scaled photo: 3.4 mm from the USB end, RST 4.4 mm from the -Y edge,
    # PRG 6.0 mm from the +Y edge (TODO: measure with calipers)
    "button_from_usb_end": 3.4,
    "rst_from_edge": 4.4,
    "prg_from_edge": 6.0,
    "button_side": 3.5,
    "button_height": 2.0,
    # Lid openings over the board. Window 1 mm larger than the glass along X and 1.7 mm
    # inside the PCB edges across; a 45° chamfer on the outside widens the viewing angle.
    # PRG is pressed through a flexible tab cut into the lid, with a nub underneath that
    # stops 0.3 mm above the switch; RST only through a pinhole, with a toothpick. Nub and
    # pinhole are stadium-shaped, stretched along X by the board length uncertainty
    "window_margin": 1.0,
    "window_width": 22.0,
    "window_chamfer": 1.2,
    "tab_length": 12.0,
    "tab_width": 6.0,
    "tab_thickness": 1.0,
    "tab_slot": 1.0,
    "nub_diameter": 4.0,
    "nub_clearance": 0.3,
    "rst_hole": 3.0,
    # Separate carrier with rails, as in the transmitter enclosure: the board slides in
    # from the USB end outside the enclosure, up to the heads, and the carrier drops onto
    # the floor pins. The slot is 0.1 mm taller than the transmitter one because the
    # header holes keep some solder after the pins are removed
    "rail_width": 2.0,
    "rail_capture": 0.6,
    "rail_side_clearance": 0.175,
    "rail_slot": 2.3,
    "rail_lip": 1.6,
    # Rails start after the chamfered corners of the USB end and clear of the back columns
    "rail_start": 6.0,
    # Tall base: it raises the board so the OLED sits just under the lid while the SMA
    # band keeps its full height. Crossbars at both ends of the rails, open in the middle
    "carrier_base": 5.0,
    "carrier_crossbar": 10.0,
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
    "antenna_hole": 6.8,  # bulkhead SMA, through the lid
    # SMA centre: 13 mm from the back wall, 6.5 mm from the +Y wall; the nut (Ø9.2 across
    # corners, estimate) clears the back column and the carrier
    "antenna_from_back": 13.0,
    "antenna_from_side": 6.5,
    # Closure: columns in the inner corners with a heat-set insert at the top; lid held by
    # M3x8 (2.4 mm of lid + 5.6 mm inside the insert)
    "column_side": 7.0,
    # 3.6 mm instead of the 3.4 mm of the transmitter: 0.3 mm per side forgives a slightly
    # off-centre insert
    "m3_hole": 3.6,
    # Hole for an M3 insert 5.7 mm long and Ø4.6 outside, with 0.8 mm spare at the bottom
    # for displaced plastic (TODO: check against the insert actually used)
    "insert_hole": 4.0,
    "insert_depth": 6.5,
    # 45° chamfer at the mouth of the hole, from Ø4.0 to Ø5.0, so the insert starts centred
    # and upright (transmitter r05)
    "insert_chamfer": 0.5,
    "lip_width": 1.2,
    "lip_height": 3.0,
}


def box(x, y, z, dx, dy, dz):
    return Part.makeBox(dx, dy, dz, V(x, y, z))


def cylinder(r, h, base, direction):
    return Part.makeCylinder(r, h, base, direction)


def stadium(x, y, z, length, width, h):
    """Slot shape along X, centred at (x, y), from z up by h."""
    r = width / 2
    if length - width < 1e-6:
        return cylinder(r, h, V(x, y, z), V(0, 0, 1))
    shape = box(x - length / 2 + r, y - r, z, length - width, width, h)
    for xc in (x - length / 2 + r, x + length / 2 - r):
        shape = shape.fuse(cylinder(r, h, V(xc, y, z), V(0, 0, 1)))
    return shape


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
    c = p["column_side"]

    # Board: USB-C at the -X wall, antenna end towards +X; carrier against the column band
    lp, wp, ep = p["board_length"], p["board_width"], p["board_thickness"]
    rail_w, cap, clr = p["rail_width"], p["rail_capture"], p["rail_side_clearance"]
    y_out0 = t + c + 0.5
    yp0 = y_out0 + rail_w
    xp0 = t + p["board_usb_wall_clearance"] + p["board_usb_overhang"]
    x_front = xp0 + lp
    zp = fl + p["carrier_base"] + p["board_bottom_components"] + p["board_clearance_below_components"]
    z_pcb_top = zp + ep
    yc_board = yp0 + wp / 2

    body = round_vertical_edges(box(0, 0, 0, L, W, hb), p["corner_radius"])
    cavity = round_vertical_edges(box(t, t, fl, lin, win, hin + 1), 1.0)
    body = body.cut(cavity)

    # Board carrier (separate part), printed with the crossbars on the bed: crossbars at the
    # ends joining the rails, rails with a slot closed at the front end and two heads that
    # drop onto the floor pins. The IPEX pigtail leaves between the heads
    slot, lip_r = p["rail_slot"], p["rail_lip"]
    z_slot = zp - (slot - ep) / 2
    z_top = z_slot + slot + lip_r
    x_start, x_end = xp0 + p["rail_start"], x_front
    y_out1 = yp0 + wp + rail_w
    base, bar, head = p["carrier_base"], p["carrier_crossbar"], p["head_side"]
    # The heads start at the end of the slot and act as the board stop
    x_head = x_end + 0.2
    pins = [(x_head + head / 2, y_out0 + head / 2), (x_head + head / 2, y_out1 - head / 2)]
    # Front crossbar and rails reach 1 mm into the heads so they fuse into one part
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

    # USB-C opening in the back wall; the connector sits on top of the board
    zc_usb = z_pcb_top + p["board_usb_height"] / 2
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

    # Columns in the inner corners, joined to the walls, with an insert from the top for the lid
    corners = [(t, t), (L - t - c, t), (t, W - t - c), (L - t - c, W - t - c)]
    centres = [(x + c / 2 - (0.6 if x == t else -0.6), y + c / 2 - (0.6 if y == t else -0.6)) for x, y in corners]
    for x, y in corners:
        body = body.fuse(box(x, y, fl, c, c, hin))
    ins_ch = p["insert_chamfer"]
    for cx, cy in centres:
        body = body.cut(cylinder(ins_r, ins_depth + 1, V(cx, cy, hb - ins_depth), V(0, 0, 1)))
        if ins_ch:
            # 45° cone running 1 mm past the top, so the cut leaves no coplanar face
            body = body.cut(Part.makeCone(ins_r, ins_r + ins_ch + 1, ins_ch + 1, V(cx, cy, hb - ins_ch)))

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

    # OLED window, measured from the antenna end of the board, which the heads locate
    ol, ow, om = p["oled_length"], p["oled_width"], p["window_margin"]
    x_glass1 = x_front - p["oled_from_front_end"]
    x_glass0 = x_glass1 - ol
    x_win0, x_win1 = x_glass0 - om, x_glass1 + om
    y_win0 = yc_board - p["window_width"] / 2
    lid = lid.cut(box(x_win0, y_win0, hb - 1, x_win1 - x_win0, p["window_width"], tl + 2))
    wc = p["window_chamfer"]
    funnel = Part.makeLoft(
        [
            Part.makePolygon([V(x_win0, y_win0, hb + tl - wc), V(x_win1, y_win0, hb + tl - wc),
                              V(x_win1, y_win0 + p["window_width"], hb + tl - wc),
                              V(x_win0, y_win0 + p["window_width"], hb + tl - wc), V(x_win0, y_win0, hb + tl - wc)]),
            Part.makePolygon([V(x_win0 - wc - 1, y_win0 - wc - 1, hb + tl + 1), V(x_win1 + wc + 1, y_win0 - wc - 1, hb + tl + 1),
                              V(x_win1 + wc + 1, y_win0 + p["window_width"] + wc + 1, hb + tl + 1),
                              V(x_win0 - wc - 1, y_win0 + p["window_width"] + wc + 1, hb + tl + 1),
                              V(x_win0 - wc - 1, y_win0 - wc - 1, hb + tl + 1)]),
        ],
        True,
    )
    lid = lid.cut(funnel)

    # Buttons: RST pinhole, PRG flexible tab. The tab is cut by a U-shaped slot, hinged at
    # its +X end, kept at 1 mm by a pocket on the inner face; the nub stands in that pocket.
    # The openings are centred between the button positions of the two board lengths
    xb = xp0 + p["button_from_usb_end"]
    stretch = p["board_length_alt"] - lp
    x_open = xb - stretch / 2
    y_rst = yp0 + p["rst_from_edge"]
    y_prg = yp0 + wp - p["prg_from_edge"]
    lid = lid.cut(stadium(x_open, y_rst, hb - 1, p["rst_hole"] + stretch, p["rst_hole"], tl + 2))
    tab_l, tab_w, tab_e, tab_s = p["tab_length"], p["tab_width"], p["tab_thickness"], p["tab_slot"]
    nub_l = p["nub_diameter"] + stretch
    x_tab0 = x_open - nub_l / 2 - 0.4
    y_tab0 = y_prg - tab_w / 2
    z_tab = hb + tl - tab_e
    pocket = box(x_tab0 - tab_s, y_tab0 - tab_s, hb - 1, tab_l + tab_s, tab_w + 2 * tab_s, z_tab - hb + 1)
    lid = lid.cut(pocket)
    u_slot = box(x_tab0 - tab_s, y_tab0 - tab_s, hb - 1, tab_l + tab_s, tab_w + 2 * tab_s, tl + 2).cut(
        box(x_tab0, y_tab0, hb - 2, tab_l + 1, tab_w, tl + 4)
    )
    lid = lid.cut(u_slot)
    z_nub = z_pcb_top + p["button_height"] + p["nub_clearance"]
    lid = lid.fuse(stadium(x_open, y_prg, z_nub, nub_l, p["nub_diameter"], z_tab - z_nub))

    # SMA antenna through the lid, in the +Y band at the back
    x_sma, y_sma = t + p["antenna_from_back"], W - t - p["antenna_from_side"]
    lid = lid.cut(cylinder(p["antenna_hole"] / 2, tl + 2, V(x_sma, y_sma, hb - 1), V(0, 0, 1)))

    # Ghost parts for visual checks (not printed)
    pcb = box(xp0, yp0, zp, lp, wp, ep)
    usb = box(
        xp0 - p["board_usb_overhang"], yc_board - p["board_usb_width"] / 2, z_pcb_top,
        7.5, p["board_usb_width"], p["board_usb_height"],
    )
    oled = box(x_glass0, yc_board - ow / 2, z_pcb_top, ol, ow, p["oled_height"])
    bs = p["button_side"]
    buttons = [box(xb - bs / 2, y - bs / 2, z_pcb_top, bs, bs, p["button_height"]) for y in (y_rst, y_prg)]
    below = p["board_bottom_components"]
    # Battery connector under the board: size from the transmitter board, position unknown
    connector = box(xp0 + 2, yc_board - 2.15, zp - below, 3.0, 4.3, below)
    ipex = box(x_front - 3.5, yc_board - 1.5, z_pcb_top, 3.0, 3.0, 2.5)
    board = pcb.fuse([usb, oled, connector, ipex] + buttons)
    # SMA bulkhead body under the lid and the nut, for the clearance check (estimates)
    sma = cylinder(4.6, 2.5, V(x_sma, y_sma, hb - 2.5), V(0, 0, 1)).fuse(
        cylinder(4.0, 9.0, V(x_sma, y_sma, hb - 2.5 - 9.0), V(0, 0, 1))
    )

    return {
        "Body": body.removeSplitter(),
        "Board_carrier": carrier.removeSplitter(),
        "Lid": lid.removeSplitter(),
        "Ghost_board": board,
        "Ghost_sma": sma,
    }, {"outer": (L, W, hb + tl)}


COLORS = {
    "Body": ((0.82, 0.84, 0.80), 0),
    "Lid": ((0.70, 0.76, 0.72), 55),
    "Board_carrier": ((0.85, 0.55, 0.20), 0),
    "Ghost_sma": ((0.25, 0.25, 0.25), 0),
    "Ghost_board": ((0.10, 0.45, 0.25), 0),
}


def build(name="WifiLora32Receiver"):
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
