import http from "k6/http";
import { check } from "k6";
import { config } from "./utils/config.js";

export const options = {
  vus: config.vus,
  duration: config.duration,
};

export default function () {
  const payload = JSON.stringify({
    email: "user@example.com",
    password: "Qwertyu1@",
  });

  const res = http.post(`${config.baseUrl}/auth/login`, payload, {
    headers: config.headers
  });

  check(res, {
    "login success": (r) => r.status === 200,
    "response time is less than 200ms": (r) => r.timings.duration < 200
  });
}
