// SPDX-License-Identifier: Apache-2.0
// Connectivity check endpoint for Tangelo OS (see docs/PRIVACY.md).
// Answers /generate_204 with an empty 204 response and logs nothing.
export default {
  fetch(request) {
    const { pathname } = new URL(request.url);
    if (pathname === '/generate_204') {
      return new Response(null, { status: 204, headers: { 'Cache-Control': 'no-store' } });
    }
    return new Response('Not found\n', { status: 404 });
  },
};
