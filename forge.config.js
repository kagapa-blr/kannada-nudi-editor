import { FusesPlugin } from '@electron-forge/plugin-fuses';
import { FuseV1Options, FuseVersion } from '@electron/fuses';

export const packagerConfig = {
  asar: true, // Package the app's source code into an ASAR archive
};

export const rebuildConfig = {};

export const makers = [
  {
    name: '@electron-forge/maker-squirrel', // For Windows (creates a .exe installer)
    config: {},
  },
  {
    name: '@electron-forge/maker-zip', // For macOS (creates a .zip file)
    platforms: ['darwin'],
  },
  {
    name: '@electron-forge/maker-deb', // For Linux (creates a .deb package)
    config: {
      options: {
        maintainer: 'ravi.ravipawar17@gmail.com',
        homepage: 'kagapa.com',
        categories: ['Utility'],
        // icon: 'path/to/icon.png', // Optional: Path to your app's icon
      },
    },
  },
  {
    name: '@electron-forge/maker-rpm', // For Linux (creates an .rpm package)
    config: {},
  },
];

export const plugins = [
  {
    name: '@electron-forge/plugin-auto-unpack-natives', // Auto-unpack native modules
    config: {},
  },
  new FusesPlugin({
    version: FuseVersion.V1, // Use Fuse version 1
    [FuseV1Options.RunAsNode]: false, // Disable running Electron as a Node.js process
    [FuseV1Options.EnableCookieEncryption]: true, // Enable cookie encryption
    [FuseV1Options.EnableNodeOptionsEnvironmentVariable]: false, // Disable NODE_OPTIONS env variable
    [FuseV1Options.EnableNodeCliInspectArguments]: false, // Disable CLI inspect arguments
    [FuseV1Options.EnableEmbeddedAsarIntegrityValidation]: true, // Enable integrity validation for ASAR
    [FuseV1Options.OnlyLoadAppFromAsar]: true, // Restrict loading only from ASAR
  }),
];
