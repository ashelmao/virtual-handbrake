import pygame
import pyvjoy
import sys

def main():
    pygame.display.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        pygame.quit()
        sys.exit(1)

    selected = 0
    for i in range(pygame.joystick.get_count()):
        js = pygame.joystick.Joystick(i)
        js.init()
        if "g920" in js.get_name().lower() or "logitech" in js.get_name().lower():
            selected = i

    joystick = pygame.joystick.Joystick(selected)
    joystick.init()

    vj = pyvjoy.VJoyDevice(1)
    vj.set_axis(pyvjoy.HID_USAGE_X, 0x0)

    prev = not joystick.get_button(14)
    vj.set_axis(pyvjoy.HID_USAGE_X, 0x8000 if prev else 0x0)
    clock = pygame.time.Clock()

    try:
        while True:
            pygame.event.pump()
            val = not joystick.get_button(14)
            if val != prev:
                vj.set_axis(pyvjoy.HID_USAGE_X, 0x8000 if val else 0x0)
                prev = val
            clock.tick(120)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
