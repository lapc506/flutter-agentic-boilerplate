-- Kong Custom Rate Limiting Plugin
--
-- This plugin implements custom rate limiting using Redis for distributed
-- rate limiting across multiple Kong instances.
--
-- Installation:
--   1. Copy this file to: /usr/local/share/lua/5.1/kong/plugins/custom-rate-limiting/
--   2. Create schema.lua for plugin configuration
--   3. Enable plugin in Kong configuration
--
-- Usage in kong.yml:
--   plugins:
--     - name: custom-rate-limiting
--       config:
--         limit: 100
--         window: 60
--         redis_host: redis
--         redis_port: 6379

local Redis = require "resty.redis"
local red = Redis:new()

local CustomRateLimiting = {}

-- Plugin configuration schema
-- This should be in a separate schema.lua file:
--[[
return {
  name = "custom-rate-limiting",
  fields = {
    { config = {
        type = "record",
        fields = {
          { limit = { type = "number", required = true, default = 100 } },
          { window = { type = "number", required = true, default = 60 } },
          { redis_host = { type = "string", required = true, default = "127.0.0.1" } },
          { redis_port = { type = "number", required = true, default = 6379 } },
          { identifier = { type = "string", required = false, default = "ip" } }, -- ip, consumer, header
        }
      }
    }
  }
}
--]]

function CustomRateLimiting:access(conf)
  -- Determine identifier based on configuration
  local identifier
  if conf.identifier == "consumer" then
    identifier = ngx.ctx.authenticated_consumer and ngx.ctx.authenticated_consumer.id or ngx.var.remote_addr
  elseif conf.identifier == "header" then
    identifier = ngx.req.get_headers()["X-API-Key"] or ngx.var.remote_addr
  else
    identifier = ngx.var.remote_addr
  end

  -- Build rate limit key
  local key = "rate_limit:" .. identifier .. ":" .. ngx.var.request_uri

  local limit = conf.limit
  local window = conf.window

  -- Connect to Redis
  red:set_timeout(1000)
  local ok, err = red:connect(conf.redis_host, conf.redis_port)

  if not ok then
    ngx.log(ngx.ERR, "Failed to connect to Redis: ", err)
    -- Fail open: allow request if Redis is unavailable
    -- For fail-closed behavior, uncomment the following:
    -- ngx.status = 503
    -- ngx.say('{"error": "Rate limiting service unavailable"}')
    -- ngx.exit(503)
    return
  end

  -- Authenticate if Redis requires password
  -- local auth_ok, auth_err = red:auth("your-redis-password")
  -- if not auth_ok then
  --   ngx.log(ngx.ERR, "Redis authentication failed: ", auth_err)
  --   return
  -- end

  -- Increment counter
  local current, err = red:incr(key)

  if not current then
    ngx.log(ngx.ERR, "Failed to increment Redis key: ", err)
    return
  end

  -- Set expiration on first request
  if current == 1 then
    red:expire(key, window)
  end

  -- Check if limit exceeded
  if current > limit then
    -- Get TTL for reset time
    local ttl = red:ttl(key)

    -- Set rate limit headers
    ngx.header["X-RateLimit-Limit"] = limit
    ngx.header["X-RateLimit-Remaining"] = 0
    ngx.header["X-RateLimit-Reset"] = ttl
    ngx.header["Retry-After"] = ttl

    -- Return rate limit error
    ngx.status = 429
    ngx.header["Content-Type"] = "application/json"
    ngx.say('{"error": "Rate limit exceeded", "retry_after": ' .. ttl .. '}')
    ngx.exit(429)
  else
    -- Set rate limit headers for successful request
    local ttl = red:ttl(key)
    ngx.header["X-RateLimit-Limit"] = limit
    ngx.header["X-RateLimit-Remaining"] = limit - current
    ngx.header["X-RateLimit-Reset"] = ttl
  end

  -- Return connection to pool
  local ok, err = red:set_keepalive(10000, 100)
  if not ok then
    ngx.log(ngx.ERR, "Failed to set Redis keepalive: ", err)
  end
end

return CustomRateLimiting
