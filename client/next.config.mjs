/** @type {import('next').NextConfig} */
const nextConfig = {
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
if (process.env.NODE_ENV === "development") {
    nextConfig.distDir = '/templates'
}
else {
    nextConfig.distDir = '../server/templates'
}
  


export default nextConfig