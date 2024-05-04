# Update-Script-Gists

This repository serves as a hub for scripts and GitHub Actions that keep your Gists up-to-date. The scripts in this repository are designed to automatically check for updates to various software and reflect those updates in the corresponding Gists.

## Current Scripts

- `update_install_golang_gist.py`: This script checks for the latest version of GoLang and updates a Gist that contains a shell script for installing Go on Linux.

## How it Works

The scripts use GitHub Actions to run on a schedule, typically every 6 hours. They can also be triggered manually if needed. When a script runs, it checks for the latest version of the software it's associated with. If a new version is found, the script updates the corresponding Gist with the new version information.

## Contributing

Contributions are welcome! If you have a script for updating a Gist with new software versions, feel free to open a pull request.

## Future Plans

We plan to add more scripts for different software in the future. Stay tuned for updates!

## License

This project is open source and available under the [MIT License](LICENSE).