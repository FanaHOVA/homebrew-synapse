# Synapse

Homebrew tap for Synapse, the installer of Neuralib packages. 

## Installation

```bash
brew tap fanahova/synapse
brew install synapse # Or fanahova/synapse/synapse
```

## Usage

In the root directory of your Neuralib project, run:

`synapse install <package_name>`

If a `synapses.json` file doesn't exist already, it will create one to store installed packages. If you do have one, you can run:

`synapse install-all` to install all packages in the `synapses.json` file

To uninstall a package:

`synapse uninstall <package_name>`