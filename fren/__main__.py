if __name__ == "__main__":
    from fren.logger import setup_logging
    setup_logging()

    try:
        from fren.app import main
        main()
    except KeyboardInterrupt:
        print("\nQUITTING!!!")
        exit(0)
