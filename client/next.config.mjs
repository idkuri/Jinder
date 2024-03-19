/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    distDir: 'templates',
    assetPrefix: '',
    async headers() {
      return [
        {
          source: '/:path*',
          headers: [
            {
              key: 'X-Content-Type-Options',
              value: 'nosniff',
            },
          ],
        },
      ];
    },
  
  };
  


export default nextConfig