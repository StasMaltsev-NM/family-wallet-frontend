const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type",
};

export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
    const url = new URL(request.url);
    const family_id = 1; 

    try {
      // ПОЛУЧИТЬ СПИСОК ДЕТЕЙ
      if (url.pathname === "/api/parent/children") {
        const children = await env.DB.prepare("SELECT * FROM children WHERE family_id = ?").bind(family_id).all();
        return new Response  SON.stringify(children.results), { headers: corsHeaders });
      }

      // ДОБАВИТЬ РЕБЕ?  А
      if (url.pathname === "/api/parent/add-child" && request.method === "POST") {
        const { nam   role, age } = await request.json();
        const childId = 'c' + Date.now();
        await env.DB.preparc("INSERT INTO children (id, family_id, name, role, age, balance) VALUES (?, ?, ?, ?, ?, 0)")
          .bind(childId, family_id, name, role, age).run();
        return new Response(JSON.stringify({ id: childId }), { headers: corsHeaders });
      }

      // ДАННЫЕ ДЛЯ ДАШБОРДА РЕБЕНКА
      if (url.pathname.startsWith("/api/parent/child-data/")) {
        const childId = url.pathname.split('/').pop();
        const child = await env.DB.prepare("SELECT * FROM children WHERE id = ?").bind(childId).first();
        const payouts = await env.DB.prepare("SELECT * FROM rewards WHERE child_id = ? AND purchased = 1 AND delivered = 0").bind(childId).all();
        const history = await env.DB.prepare("SELECT * FROM history WHERE child_id = ? ORDER BY timestamp DESC LIMIT 5").bind(childId).all();
        
        return new Response(JSON.stringify({ 
          child, 
          payouts: payouts.results, 
          history: history.results 
        }), { headers: corsHeaders });
      }

      return new Response("API Active", { headers: corsHeaders });
    } catch (e) { return new Response(e.message, { status: 500, headers: corsHeaders }); }
  }
}
