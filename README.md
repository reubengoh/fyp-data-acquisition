# fyp-data-acquisition

This is my NTU EEE final year project.
It is a cloud-based data acquisition device created for a electrical control panel to collect data
and send it to cloud. The data collected are binary and analog signals from the relays of the control
panel and the water pressure sensor. The cloud service that this project uses is AWS IoT Core. Data 
collected from the raspberry pi via the GPIO inputs, will be saved on a local CSV file. Also, it will
be sent to the cloud via the MQTT Protocol.

More information of this project can be found in my final year report that I would be uploading soon.
Feel free to use the code for your cloud-based applications. 

![FYP Overall System Architecture](https://github.com/reubengoh/fyp-data-acquisition/assets/93382264/b588b577-160c-48e9-93d4-0593022db6ab)
