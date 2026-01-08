export const config = {
  vus: 10,          // concurrent users
  duration: '30s',  // test duration
  baseUrl: "http://127.0.0.1:8000/api",
  thresholds: {
    http_req_duration: ["p(95)<800"], // 95% under 800ms
    http_req_failed: ["rate<0.01"],
    http_response_time: ["p(95)<800"], // 95% under 800ms
  },
  headers: {
    "Content-Type": "application/json",
  },
};
