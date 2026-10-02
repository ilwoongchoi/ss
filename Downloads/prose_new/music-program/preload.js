const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  platform: process.platform,
  versions: process.versions,
  onRequestSaveState: (callback) => ipcRenderer.on('request-save-state', () => callback()),
  sendSaveStateData: (data) => ipcRenderer.send('save-state-data', data),
  onLoadStateData: (callback) => ipcRenderer.on('load-state-data', (event, data) => callback(data))
});
