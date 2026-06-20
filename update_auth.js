import fs from 'fs';
import path from 'path';
import os from 'os';
import { execSync } from 'child_process';

const cookieStr = `_ga=GA1.1.2034374334.1755262763; HSID=ALek81sLCr-ndPszk; SSID=AZodfLBJJmpAG1eAE; APISID=95UL-CoDt4PDRRhO/A6lPCFp-gC6L2-Jnk; SAPISID=qFNriS7ohZRSaDNO/APANTO5o0nggULg9c; __Secure-1PAPISID=qFNriS7ohZRSaDNO/APANTO5o0nggULg9c; __Secure-3PAPISID=qFNriS7ohZRSaDNO/APANTO5o0nggULg9c; OSID=g.a000-QjbsoE8UwHWSjbq-i_rRXhN4u9j0uHaPK9i_5Er_DGFgknOdeqJ_sPOiLpz5u0ZwgBtVgACgYKAQESARISFQHGX2MiOxsXZnzUWTiqSphPr-RtshoVAUF8yKocx_Lkgn703UR04fY48bs70076; __Secure-OSID=g.a000-QjbsoE8UwHWSjbq-i_rRXhN4u9j0uHaPK9i_5Er_DGFgknOXVpGqEkJ36mSviS-NpLqiAACgYKAUsSARISFQHGX2Mi5YjnATjGxlt80yVTmT1cBRoVAUF8yKoEMJGAhlXbNTY7W0gQhyiN0076; _gcl_au=1.1.1524712962.1780496102; __Secure-BUCKET=CNEE; SEARCH_SAMESITE=CgQIiqEB; SID=g.a000_QjbsmWJ08TYWz54sii_CXwxk5rFDCRkKfOavPPDXLldZ6Bo7XMqXBklDvK1K6bhXPHxhAACgYKAaYSARISFQHGX2MidJ7yKOQsOLsIbgw9isPXvBoVAUF8yKqTT2TT61Nw2kXa2UjXXeRN0076; __Secure-1PSID=g.a000_QjbsmWJ08TYWz54sii_CXwxk5rFDCRkKfOavPPDXLldZ6BoMkYhrxlRGF3Wt6Nd0DexvAACgYKAesSARISFQHGX2MiSlVQ2yU8fP3cJxI4G8DGzxoVAUF8yKpyQv_HQ1r9VD7RT_CUfP4B0076; __Secure-3PSID=g.a000_QjbsmWJ08TYWz54sii_CXwxk5rFDCRkKfOavPPDXLldZ6BompyGTtpj3_MyU4IZbPLNIgACgYKAecSARISFQHGX2Mif4cn_Kmo3wGLmIYzEfAduxoVAUF8yKoTKPCFXH_SkuBhfywn7y680076; S=billing-ui-v3=4sB2L2t_xX4chk8mO4jrjttc8TXI-uPd:billing-ui-v3-efe=4sB2L2t_xX4chk8mO4jrjttc8TXI-uPd; AEC=AdJVEav_XyesKnwAO2Jlefu9tNbvzjcNxBkhNzZR9qZYP2mZeweVFbooubk; NID=532=H78iZQ3WDyjOJcXuvzrTC74dUaseG7pmqKFWBUmz1Xv7vheFbY1m2bSlTqSej85EsFnHLG0_iJlIUyb32EsT5lKtP8ve4PmqKm3HKtUlLfXKY5Mdz-RAQWg1KUWBvbJnVkqqf0WdjqYV188-1SqwCawDJqFbmLo7JeABt_5go1efRLydE2AhDsmuhunTP-JDXcbugah59m2phLNxczgZ7rkI0YLVM-v_el7scOFycydEpMrQ8iAAWcCLSlpl7uR69vK0aHd2jWL1oLrEsrsidqLrErBc-ViJMuMRZC44NWRMeSg57Vt4gBggXDpIOs7ztq0_fdx4jqX2bDDyh9Iqgm7wTLO-nKCSSg-SHwEI0Oo2yK5dEZrvjS6VEGqFmA_OKixtQCNC6ag2jhTzaKDQR8Jo--hfouUQjoipSmr2-Ry8PhMdkRJ4XQCDwuDCvm0sqKC_hZq5Dxel764rYrnEXGUCACbH1G2pFJsFUuMyeBq586nHs7bXYz8ziq_Pu5Vyi8ORjZY0uWAj2JyWMOlPxaFb8qU1nBdE3q_NQmOkynvnpAqS189aZkjx9BNsTjVey2y2cjhSyvU_dacYtD-HWCem9FIxiTiAM1RzNK39B30O98fLxwIiLUu89ro11PDpLZ_ILROKvcIwmT3MpmugBllma47dInt5AogUF67-69v9boPHTmCbBexGppdcyQ2VuSVGoLtsABsq5B8_IRzQXafoRT82wxyjz0J6lc9IzVGHOi1HvLShpHk7T6p18pCV13uHHGGOm43mzxsiMqEKE7x3fXUoX4MHUbwNW10EDwTtvfziG_sHVE1aMaf25gVOrgJ4UULD; __Secure-1PSIDTS=sidts-CjcByojQU9YgM1axKYUQJVHtlCmMVTXFZZdgU4nUTNVOUgP6FfpCcGlI-U14gIL6gXoy8sZxesSjEAA; __Secure-1PSIDRTS=sidts-CjcByojQU9YgM1axKYUQJVHtlCmMVTXFZZdgU4nUTNVOUgP6FfpCcGlI-U14gIL6gXoy8sZxesSjEAA; __Secure-3PSIDTS=sidts-CjcByojQU9YgM1axKYUQJVHtlCmMVTXFZZdgU4nUTNVOUgP6FfpCcGlI-U14gIL6gXoy8sZxesSjEAA; __Secure-3PSIDRTS=sidts-CjcByojQU9YgM1axKYUQJVHtlCmMVTXFZZdgU4nUTNVOUgP6FfpCcGlI-U14gIL6gXoy8sZxesSjEAA; _ga_W0LDH41ZCB=GS2.1.s1781967171$o106$g0$t1781967171$j60$l0$h0; SIDCC=AKEyXzU5BrVmhieWWpxQuhtQLA_nykhAeUI-xbfpUgNkO6ywOThP_W3h-0oAaXkdwYQRPVBp4w; __Secure-1PSIDCC=AKEyXzVJzU5ylgfgqSzeAUKPgmBi_t9vAshkTJddu0PNDuKxAfUNszPsCDtCCzq3nfrVcCxtEL0; __Secure-3PSIDCC=AKEyXzWAj8gqV-CY91x-R4xx_uzuVhHttQSH2F4bIU_c_gFUdGfN8lsKxHX_1s31mNCvgKzJmOg`;

// Parse cookie string to key-value object
const cookies = {};
cookieStr.split(';').forEach(c => {
  const parts = c.trim().split('=');
  if (parts.length >= 2) {
    const name = parts[0];
    const value = parts.slice(1).join('=');
    cookies[name] = value;
  }
});

const authDir = path.join(os.homedir(), '.notebooklm-mcp');
const authPath = path.join(authDir, 'auth.json');

if (!fs.existsSync(authDir)) {
  fs.mkdirSync(authDir, { recursive: true });
}

let existingData = { cookies: {}, csrf_token: "" };
if (fs.existsSync(authPath)) {
  try {
    existingData = JSON.parse(fs.readFileSync(authPath, 'utf8'));
  } catch (e) {
    console.log("Could not parse existing auth.json, overwriting...");
  }
}

// Update cookies and save
existingData.cookies = cookies;
existingData.updated_at = new Date().toISOString();
fs.writeFileSync(authPath, JSON.stringify(existingData, null, 2));
console.log(`Successfully updated cookies in ${authPath}`);
