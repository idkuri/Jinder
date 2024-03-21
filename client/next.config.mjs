/** @type {import('next').NextConfig} */
const nextConfig = {
    distDir: '../server/templates',
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

if (process.env.NODE_ENV === 'production') {
    nextConfig.output = 'export';
}
  


export default nextConfig