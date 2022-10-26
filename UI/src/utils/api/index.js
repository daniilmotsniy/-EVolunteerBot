/**
 * Centralized utilities to work with API methods
 */
 import API from './API';
 import {
  ORDER_STATUS
} from './constants';
const API_HOST = window.location.hostname;
const API_PROTOCOL = window.location.protocol;
const API_URL = `${API_PROTOCOL}//${API_HOST}`;


const api = new API(API_URL);
api.setUp();
export {
  api,
  API,
  ORDER_STATUS
};