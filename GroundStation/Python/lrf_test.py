from djiInterfaceLite import DJIInterfaceLite
import sys
import time
import requests


def prompt_float(label):
    raw = input(f"Enter desired gimbal {label} angle (in degrees): ")
    try:
        return float(raw)
    except ValueError:
        print(f"Invalid input. Please enter a numeric value for the {label} angle.")
        return None


def safe(call, *args, **kwargs):
    """Run a DJI interface call, printing a friendly message on connection errors."""
    try:
        return call(*args, **kwargs)
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: could not reach RC. {e.__class__.__name__}")
        return None
    except requests.exceptions.Timeout:
        print("Connection error: request timed out.")
        return None


def main():
    ip_rc = sys.argv[1] if len(sys.argv) == 2 else "172.20.10.6"
    dji_interface = DJIInterfaceLite(ip_rc)
    print(f"Targeting RC at {ip_rc} ...")

    menu = (
        "Enter a command:\n"
        "  p - set gimbal pitch\n"
        "  y - set gimbal yaw\n"
        "  t - trigger LRF\n"
        "  d - get LRF distance\n"
        "  g - get LRF target point\n"
        "  q - quit\n"
        "> "
    )

    while True:
        usr_input = input(menu).strip().lower()

        if usr_input == "q":
            break

        elif usr_input == "p":
            pitch_angle = prompt_float("pitch")
            if pitch_angle is not None:
                if safe(dji_interface.requestSendGimbalPitch, pitch_angle) is not None:
                    print(f"Gimbal pitch set to {pitch_angle} degrees...")
            time.sleep(1)

        elif usr_input == "y":
            yaw_angle = prompt_float("yaw")
            if yaw_angle is not None:
                if safe(dji_interface.requestSendGimbalYaw, yaw_angle) is not None:
                    print(f"Gimbal yaw set to {yaw_angle} degrees...")
            time.sleep(1)

        elif usr_input == "t":
            if safe(dji_interface.requestSendTriggerLRF) is not None:
                print("LRF triggered. Allow ~1s for first measurement.")
            time.sleep(1)

        elif usr_input == "d":
            distance = safe(dji_interface.requestLRFDistance)
            if distance is None:
                print("No LRF distance available yet. Trigger the LRF first (or check connection).")
            else:
                print(f"LRF distance: {distance:.2f} m")

        elif usr_input == "g":
            target = safe(dji_interface.requestLRFTargetPoint)
            if target is None:
                print("No LRF target point available yet. Trigger the LRF first (or check connection).")
            else:
                lat, lon, alt = target
                print(f"LRF target point: lat={lat:.7f}, lon={lon:.7f}, alt={alt:.2f} m")

        else:
            print("Unknown command. Try p, y, t, d, g, or q.")


if __name__ == "__main__":
    main()
