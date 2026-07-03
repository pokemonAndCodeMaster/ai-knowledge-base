'use strict';

const https = require('node:https');
const path = require('node:path');

const happyRoot = process.env.HAPPY_CODER_ROOT;
if (!happyRoot) {
  throw new Error('未设置 HAPPY_CODER_ROOT');
}
const { HttpsProxyAgent } = require(path.join(
  happyRoot,
  'node_modules/https-proxy-agent',
));

const proxyUrl =
  process.env.HTTPS_PROXY ||
  process.env.https_proxy ||
  process.env.ALL_PROXY ||
  process.env.all_proxy;

if (!proxyUrl) {
  throw new Error('未设置 HTTPS_PROXY/https_proxy/ALL_PROXY/all_proxy');
}

const proxyAgent = new HttpsProxyAgent(proxyUrl);
const originalRequest = https.request;

https.request = function requestWithHappyProxy(...args) {
  const optionsIndex = typeof args[0] === 'string' || args[0] instanceof URL ? 1 : 0;
  const options = args[optionsIndex];

  if (options && typeof options === 'object') {
    const hostname = options.hostname || options.host;
    if (hostname === 'api.cluster-fluster.com') {
      const proxiedOptions = { ...options, agent: proxyAgent };
      delete proxiedOptions.createConnection;
      args[optionsIndex] = proxiedOptions;
    }
  }

  return originalRequest.apply(this, args);
};
