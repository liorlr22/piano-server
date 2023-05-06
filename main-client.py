from lib.visuals import ClientApp


# TODO: Add GUI Client
#     - Where to connect
# TODO: Add Play MIDI
#     - Create Midi FILE
#     - add midi track with same properties
#     - add midi message(s)
#     - Play Midi FILE

def main() -> None:
    app = ClientApp()
    app.run()


if __name__ == '__main__':
    main()
