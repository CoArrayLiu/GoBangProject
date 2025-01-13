import axios from "axios";
//import router from "../router"


const service = axios.create({
    baseURL : "http://hbyc-n2-i101-p7860.easy-ai.cloud:8800"+"/api",
    //baseURL : "http://d.easy-ai.cloud:8000"+"/api",
    //baseURL : "http://localhost:8000"+"/api",
    timeout : 60000,
    headers: {
        'Content-Type': 'application/json',
      },
})


export default{
    service
};