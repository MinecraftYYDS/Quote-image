export async function onRequest(context) {
  const url = new URL(context.request.url);
  const qq = url.searchParams.get('qq');

  if (!qq || !/^\d{4,12}$/.test(qq)) {
    return new Response('Invalid QQ number', { status: 400 });
  }

  const avatarUrl = `https://q2.qlogo.cn/headimg_dl?dst_uin=${qq}&spec=5`;

  try {
    const resp = await fetch(avatarUrl, {
      headers: { 'User-Agent': 'Mozilla/5.0' },
    });

    return new Response(resp.body, {
      status: resp.status,
      headers: {
        'Content-Type': resp.headers.get('Content-Type') || 'image/jpeg',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=3600',
      },
    });
  } catch {
    return new Response('Failed to fetch avatar', { status: 502 });
  }
}
