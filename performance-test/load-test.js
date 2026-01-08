import http from 'k6/http';
import { check, sleep } from 'k6';
import { config } from "./utils/config.js";


export const options = {
  vus: config.vus,
  duration: config.duration,
};

export default function () {
  // Test the /products/ endpoint
  let res = http.get(`${config.baseUrl}/products/`);

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time is less than 200ms': (r) => r.timings.duration < 200,
    'response contains products array': (r) => JSON.parse(r.body).results instanceof Array
  });

  sleep(1); // Wait 1s between iterations
}