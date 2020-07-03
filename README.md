## This library is made up of code from university course repository from a LNU summer course
Course repository link: https://github.com/iot-lnu/applied-iot-20

#### Code for the blinking lights in Node-Red
'''javascript=16
if(msg.payload.home_sensor.co2 < 1000)
{
    msg = { payload: 
        {    
            alert: 0  
        } 
    };
}
else if(msg.payload.home_sensor.co2 >= 1000 && msg.payload.home_sensor.co2 < 1400)
{
    msg = { payload: 
        {    
            alert: 1  
        } 
    };
}
else if (msg.payload.home_sensor.co2 >= 1400 && msg.payload.home_sensor.co2 < 2000)
{
    msg = { payload: 
        {    
            alert: 2  
        } 
    };
}
else if (msg.payload.home_sensor.co2 >= 2000)
{
    msg = { payload: 
        {    
            alert: 3  
        } 
    };
}
return msg;
'''
