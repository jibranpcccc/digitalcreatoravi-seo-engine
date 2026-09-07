/**
 * nginx-grok-parser
 * Live Interactive Web App: https://groklogtester.pages.dev/
 */

const NGINX_REGEX = /^(\S+) \S+ (\S+) \[([^\]]+)\] "(\S+) (\S+) ([^"]+)" (\d{3}) (\d+) "([^"]*)" "([^"]*)"/;

function parseNginxLog(line) {
  const match = NGINX_REGEX.exec(line.trim());
  if (!match) return null;
  return {
    clientIp: match[1],
    remoteUser: match[2],
    timestamp: match[3],
    method: match[4],
    path: match[5],
    httpVersion: match[6],
    statusCode: parseInt(match[7], 10),
    bodyBytes: parseInt(match[8], 10),
    referrer: match[9],
    userAgent: match[10]
  };
}

module.exports = { parseNginxLog };
