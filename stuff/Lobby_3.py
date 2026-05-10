import pygame
import sys
import random
import math

pygame.display.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SWAT Force")
clock = pygame.time.Clock()

# --- Farben ---
PANEL_BG     = (35, 28, 20)
BTN_BASE     = (55, 45, 32)
BTN_HOVER    = (95, 82, 58)
BTN_SHADOW   = (18, 14, 8)
BTN_BORDER   = (145, 122, 82)
PANEL_BORDER = (100, 85, 60)
PANEL_LIGHT  = (120, 105, 78)
WHITE        = (255, 255, 255)
YELLOW       = (255, 215, 50)
ORANGE       = (225, 135, 35)
RED          = (190, 40, 40)

# --- Save-Menu Farben (braun, warm) ---
SAVE_BG          = (42, 28, 14)       # dunkles Braun Overlay
SAVE_PANEL       = (80, 55, 30)       # Panel-Hintergrund
SAVE_PANEL_LIGHT = (115, 82, 48)      # helle Kante oben/links
SAVE_PANEL_DARK  = (28, 18, 8)        # dunkle Kante unten/rechts
SAVE_PANEL_BORDER= (160, 118, 65)     # Rand
SAVE_SLOT_BASE   = (60, 40, 20)       # leerer Slot
SAVE_SLOT_FILLED = (72, 50, 25)       # befüllter Slot
SAVE_SLOT_HOVER  = (100, 72, 38)      # Slot hover
SAVE_SLOT_SEL    = (120, 88, 45)      # ausgewählt
SAVE_SLOT_BORDER = (140, 105, 55)
SAVE_SLOT_EMPTY_TXT = (110, 85, 50)
NEW_BTN_BASE     = (90, 60, 28)
NEW_BTN_HOVER    = (130, 92, 42)
NEW_BTN_BORDER   = (190, 148, 80)
CREAM            = (235, 210, 165)
CREAM_DIM        = (175, 148, 105)
GOLD             = (210, 170, 70)

P = 8
AA = False

# --- Fonts ---
font_big   = pygame.font.Font(None, 74)
font_med   = pygame.font.Font(None, 38)
font_small = pygame.font.Font(None, 24)
font_btn   = pygame.font.Font(None, 30)
font_tiny  = pygame.font.Font(None, 20)

def pixel_text(surface, text, font, color, x, y, shadow=True):
    if shadow:
        s = font.render(text, AA, (0, 0, 0))
        surface.blit(s, (x + 2, y + 2))
    t = font.render(text, AA, color)
    surface.blit(t, (x, y))

def pixel_text_center(surface, text, font, color, cx, y, shadow=True):
    t = font.render(text, AA, color)
    pixel_text(surface, text, font, color, cx - t.get_width() // 2, y, shadow)

# --- Panel-Rahmen Lobby ---
def draw_pixel_panel(surface, x, y, w, h, hover=False):
    bg = BTN_HOVER if hover else BTN_BASE
    pygame.draw.rect(surface, bg, (x, y, w, h))
    light = (120, 105, 75) if not hover else (145, 128, 95)
    pygame.draw.rect(surface, light,      (x, y, w, 3))
    pygame.draw.rect(surface, light,      (x, y, 3, h))
    pygame.draw.rect(surface, BTN_SHADOW, (x, y + h - 3, w, 3))
    pygame.draw.rect(surface, BTN_SHADOW, (x + w - 3, y, 3, h))
    pygame.draw.rect(surface, BTN_BORDER if hover else PANEL_BORDER, (x, y, w, h), 2)

def draw_title_panel(surface, x, y, w, h):
    pygame.draw.rect(surface, PANEL_BG,    (x, y, w, h))
    pygame.draw.rect(surface, PANEL_LIGHT, (x, y, w, 4))
    pygame.draw.rect(surface, PANEL_LIGHT, (x, y, 4, h))
    pygame.draw.rect(surface, BTN_SHADOW,  (x, y + h - 4, w, 4))
    pygame.draw.rect(surface, BTN_SHADOW,  (x + w - 4, y, 4, h))
    pygame.draw.rect(surface, BTN_BORDER,  (x, y, w, h), 3)

# --- Braunes Panel mit runden Ecken ---
def draw_brown_panel(surface, x, y, w, h, radius=16):
    """Zeichnet ein braunes Panel mit runden Ecken."""
    rect = pygame.Rect(x, y, w, h)
    # Schatten
    shadow_rect = pygame.Rect(x + 5, y + 6, w, h)
    shadow_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(shadow_surf, (0, 0, 0, 90), (0, 0, w, h), border_radius=radius)
    surface.blit(shadow_surf, (x + 5, y + 6))
    # Hauptfläche
    pygame.draw.rect(surface, SAVE_PANEL, rect, border_radius=radius)
    # Helle obere/linke Kante
    pygame.draw.rect(surface, SAVE_PANEL_LIGHT, rect, width=3, border_radius=radius)
    # Überschreibe unten/rechts mit dunkler Farbe
    pygame.draw.line(surface, SAVE_PANEL_DARK, (x + radius, y + h - 2), (x + w - radius, y + h - 2), 3)
    pygame.draw.line(surface, SAVE_PANEL_DARK, (x + w - 2, y + radius), (x + w - 2, y + h - radius), 3)
    # Äusserer Rand
    pygame.draw.rect(surface, SAVE_PANEL_BORDER, rect, width=2, border_radius=radius)

# --- Slot zeichnen ---
def draw_save_slot(surface, x, y, w, h, save_data, hovered, selected, radius=10):
    if selected:
        col = SAVE_SLOT_SEL
    elif hovered:
        col = SAVE_SLOT_HOVER
    elif save_data:
        col = SAVE_SLOT_FILLED
    else:
        col = SAVE_SLOT_BASE

    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, col, rect, border_radius=radius)
    pygame.draw.rect(surface, SAVE_SLOT_BORDER if (hovered or selected) else (90, 65, 32),
                     rect, width=2, border_radius=radius)

    if save_data:
        # Schild-Icon (simpel)
        sx, sy = x + 10, y + h // 2 - 10
        pygame.draw.rect(surface, GOLD, (sx, sy, 18, 20), border_radius=4)
        pygame.draw.rect(surface, (160, 120, 40), (sx, sy, 18, 20), width=2, border_radius=4)
        t_name = font_small.render(save_data["name"], AA, CREAM)
        surface.blit(t_name, (x + 35, y + 8))
        t_info = font_tiny.render(f"Level {save_data['level']}  |  {save_data['missions']} Missionen", AA, CREAM_DIM)
        surface.blit(t_info, (x + 35, y + 28))
    else:
        t = font_small.render("- Leerer Slot -", AA, SAVE_SLOT_EMPTY_TXT)
        surface.blit(t, (x + w // 2 - t.get_width() // 2, y + h // 2 - t.get_height() // 2))

# --- Save-Menu State ---
class SaveMenu:
    MAX_SLOTS = 5

    def __init__(self):
        self.saves = [
            {"name": "Alpha Squad",   "level": 7,  "missions": 12},
            {"name": "Bravo Unit",    "level": 3,  "missions": 4},
            None,
            None,
            None,
        ]
        self.selected = 0
        self.hovered_slot = -1
        self.new_name = ""
        self.typing = False
        self.new_btn_hovered = False
        self.close_hovered = False
        self.load_btn_hovered = False

        # Layout
        self.mx      = WIDTH // 2 - 370
        self.my      = 80
        self.mw      = 740
        self.mh      = 460
        # Linkes Panel
        self.lx = self.mx + 18
        self.ly = self.my + 55
        self.lw = 340
        self.lh = 380
        # Rechtes Panel
        self.rx = self.mx + 18 + 340 + 16
        self.ry = self.my + 55
        self.rw = 340
        self.rh = 380
        # Slot-Dimensionen
        self.slot_h  = 52
        self.slot_gap = 10

    def get_slot_rect(self, i):
        y = self.ly + 42 + i * (self.slot_h + self.slot_gap)
        return pygame.Rect(self.lx + 12, y, self.lw - 24, self.slot_h)

    def get_new_btn_rect(self):
        return pygame.Rect(self.rx + 20, self.ry + self.rh - 60, self.rw - 40, 44)

    def get_load_btn_rect(self):
        return pygame.Rect(self.rx + 20, self.ry + self.rh - 112, self.rw - 40, 44)

    def get_close_rect(self):
        return pygame.Rect(self.mx + self.mw - 38, self.my + 10, 28, 28)

    def handle_event(self, event, mouse_pos):
        """Gibt True zurück wenn Menü geschlossen werden soll."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Schliessen
            if self.get_close_rect().collidepoint(mouse_pos):
                return True
            # Slot auswählen
            for i in range(self.MAX_SLOTS):
                if self.get_slot_rect(i).collidepoint(mouse_pos):
                    self.selected = i
                    self.typing = False
                    self.new_name = ""
            # Laden-Button
            if self.get_load_btn_rect().collidepoint(mouse_pos):
                if self.saves[self.selected]:
                    print(f"Lade Safe: {self.saves[self.selected]['name']}")
            # Neuer Safe Button
            if self.get_new_btn_rect().collidepoint(mouse_pos):
                self.typing = True
                self.new_name = ""

        if event.type == pygame.KEYDOWN and self.typing:
            if event.key == pygame.K_RETURN:
                if self.new_name.strip():
                    # In ausgewählten leeren Slot speichern
                    slot = self.selected
                    if self.saves[slot] is not None:
                        # Nächsten leeren Slot suchen
                        for i in range(self.MAX_SLOTS):
                            if self.saves[i] is None:
                                slot = i
                                break
                    self.saves[slot] = {"name": self.new_name.strip(),
                                        "level": 1, "missions": 0}
                    self.selected = slot
                self.typing = False
                self.new_name = ""
            elif event.key == pygame.K_ESCAPE:
                self.typing = False
                self.new_name = ""
            elif event.key == pygame.K_BACKSPACE:
                self.new_name = self.new_name[:-1]
            else:
                if len(self.new_name) < 16:
                    self.new_name += event.unicode

        return False

    def update_hover(self, mouse_pos):
        self.hovered_slot = -1
        for i in range(self.MAX_SLOTS):
            if self.get_slot_rect(i).collidepoint(mouse_pos):
                self.hovered_slot = i
        self.new_btn_hovered  = self.get_new_btn_rect().collidepoint(mouse_pos)
        self.load_btn_hovered = self.get_load_btn_rect().collidepoint(mouse_pos)
        self.close_hovered    = self.get_close_rect().collidepoint(mouse_pos)

    def draw(self, surface, tick):
        # Dunkles Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surface.blit(overlay, (0, 0))

        # Haupt-Rahmen
        draw_brown_panel(surface, self.mx, self.my, self.mw, self.mh, radius=20)

        # Titel
        pixel_text_center(surface, "SPEICHERSTAENDE", font_med, GOLD, self.mx + self.mw // 2, self.my + 14)

        # Trennlinie
        pygame.draw.line(surface, SAVE_PANEL_BORDER,
                         (self.mx + 20, self.my + 48),
                         (self.mx + self.mw - 20, self.my + 48), 2)

        # --- Linkes Panel: Saves ---
        draw_brown_panel(surface, self.lx, self.ly, self.lw, self.lh, radius=14)
        pixel_text_center(surface, "MEINE SAVES", font_small, CREAM_DIM, self.lx + self.lw // 2, self.ly + 12)

        for i in range(self.MAX_SLOTS):
            r = self.get_slot_rect(i)
            draw_save_slot(surface, r.x, r.y, r.w, r.h,
                           self.saves[i],
                           self.hovered_slot == i,
                           self.selected == i)

        # --- Rechtes Panel: Neuer Safe / Info ---
        draw_brown_panel(surface, self.rx, self.ry, self.rw, self.rh, radius=14)
        pixel_text_center(surface, "NEUER SAVE", font_small, CREAM_DIM, self.rx + self.rw // 2, self.ry + 12)

        pygame.draw.line(surface, (100, 72, 38),
                         (self.rx + 16, self.ry + 36),
                         (self.rx + self.rw - 16, self.ry + 36), 1)

        # Info zum ausgewählten Slot
        sel_save = self.saves[self.selected]
        info_y = self.ry + 50
        if sel_save:
            pixel_text_center(surface, "Ausgewaehlt:", font_tiny, CREAM_DIM, self.rx + self.rw // 2, info_y)
            pixel_text_center(surface, sel_save["name"],  font_small, CREAM,     self.rx + self.rw // 2, info_y + 18)
            pixel_text_center(surface, f"Level {sel_save['level']}", font_tiny, GOLD, self.rx + self.rw // 2, info_y + 40)
            pixel_text_center(surface, f"{sel_save['missions']} Missionen abgeschlossen",
                              font_tiny, CREAM_DIM, self.rx + self.rw // 2, info_y + 58)
        else:
            pixel_text_center(surface, "Leerer Slot", font_small, SAVE_SLOT_EMPTY_TXT,
                              self.rx + self.rw // 2, info_y + 20)

        # Eingabefeld wenn typing
        if self.typing:
            inp_rect = pygame.Rect(self.rx + 20, self.ry + 145, self.rw - 40, 38)
            pygame.draw.rect(surface, SAVE_SLOT_BASE, inp_rect, border_radius=8)
            blink = (tick // 30) % 2 == 0
            display = self.new_name + ("|" if blink else "")
            t = font_small.render(display if display else " ", AA, CREAM)
            surface.blit(t, (inp_rect.x + 8, inp_rect.y + 9))
            pygame.draw.rect(surface, SAVE_SLOT_HOVER, inp_rect, width=2, border_radius=8)
            pixel_text_center(surface, "Name eingeben + Enter", font_tiny, CREAM_DIM,
                              self.rx + self.rw // 2, self.ry + 192)
        else:
            pixel_text_center(surface, "Klicke 'Neuer Save'", font_tiny, SAVE_SLOT_EMPTY_TXT,
                              self.rx + self.rw // 2, self.ry + 158)
            pixel_text_center(surface, "um einen neuen Safe", font_tiny, SAVE_SLOT_EMPTY_TXT,
                              self.rx + self.rw // 2, self.ry + 175)
            pixel_text_center(surface, "zu erstellen.", font_tiny, SAVE_SLOT_EMPTY_TXT,
                              self.rx + self.rw // 2, self.ry + 192)

        # Laden-Button (rechts)
        lr = self.get_load_btn_rect()
        load_col = NEW_BTN_HOVER if self.load_btn_hovered else NEW_BTN_BASE
        can_load = sel_save is not None
        load_col_use = load_col if can_load else (45, 32, 18)
        pygame.draw.rect(surface, load_col_use, lr, border_radius=10)
        pygame.draw.rect(surface, NEW_BTN_BORDER if can_load else (70, 52, 28), lr, width=2, border_radius=10)
        ltxt_col = CREAM if can_load else SAVE_SLOT_EMPTY_TXT
        pixel_text_center(surface, "[ LADEN ]", font_btn, ltxt_col, lr.centerx, lr.y + 11)

        # Neuer-Safe-Button (rechts)
        nr = self.get_new_btn_rect()
        nb_col = NEW_BTN_HOVER if self.new_btn_hovered else NEW_BTN_BASE
        pygame.draw.rect(surface, nb_col, nr, border_radius=10)
        pygame.draw.rect(surface, NEW_BTN_BORDER, nr, width=2, border_radius=10)
        pixel_text_center(surface, "[ NEUER SAVE ]", font_btn, YELLOW, nr.centerx, nr.y + 11)

        # Schliessen-Button
        cr = self.get_close_rect()
        close_col = (130, 40, 40) if self.close_hovered else (90, 30, 30)
        pygame.draw.rect(surface, close_col, cr, border_radius=6)
        pygame.draw.rect(surface, (200, 80, 80), cr, width=2, border_radius=6)
        pixel_text_center(surface, "X", font_small, WHITE, cr.centerx, cr.y + 5, shadow=False)


# --- Lobby Buttons ---
cx = WIDTH // 2

buttons = {
    "start":    Button("[ START ]",    cx, 295) if False else None,
    "settings": None,
    "quit":     None,
}

# Neu definieren ohne den obigen Fehler
class Button:
    def __init__(self, text, cx, y, w=280, h=46):
        self.text = text
        self.rect = pygame.Rect(cx - w // 2, y, w, h)
        self.hovered = False

    def draw(self, surface):
        draw_pixel_panel(surface, self.rect.x, self.rect.y,
                         self.rect.w, self.rect.h, self.hovered)
        col = YELLOW if self.hovered else WHITE
        pixel_text_center(surface, self.text, font_btn, col,
                          self.rect.centerx, self.rect.y + 11)

    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)

    def is_clicked(self, pos, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(pos))

buttons = {
    "start":    Button("[ START ]",      cx, 295),
    "settings": Button("[ WATCH CP ]",   cx, 357),
    "quit":     Button("[ BEENDEN ]",    cx, 419),
}

save_menu = SaveMenu()
show_save_menu = False
tick = 0

def run_lobby():
    global tick, show_save_menu

    while True:
        clock.tick(FPS)
        tick += 1
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if show_save_menu:
                closed = save_menu.handle_event(event, mouse_pos)
                if closed:
                    show_save_menu = False
            else:
                for name, btn in buttons.items():
                    if btn.is_clicked(mouse_pos, event):
                        if name == "quit":
                            pygame.quit(); sys.exit()
                        elif name == "start":
                            show_save_menu = True
                        elif name == "settings":
                            print("Watch CP geöffnet")


        # Titel
        pw, ph = 440, 92
        draw_title_panel(screen, cx - pw // 2, 55, pw, ph)
        pixel_text_center(screen, "SWAT  FORCE",         font_big,   YELLOW, cx, 80)
        pixel_text_center(screen, "TACTICAL OPERATIONS", font_small, ORANGE, cx, 129)

        if show_save_menu:
            save_menu.update_hover(mouse_pos)
            save_menu.draw(screen, tick)
        else:
            for btn in buttons.values():
                btn.check_hover(mouse_pos)
                btn.draw(screen)

        pygame.display.flip()

run_lobby()