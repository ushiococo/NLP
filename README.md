# NLP
1. Extract data from huge dataset using extract.py
2. Use sample data to train the dataset to model
![image](https://user-images.githubusercontent.com/61874750/202937690-0e335f9d-32c1-4584-b511-5c18fa071a88.png)
3. test the data with the trainmodel
![image](https://user-images.githubusercontent.com/61874750/202945369-85f3c6db-d268-4cc3-8a67-2fc440100b2b.png)

4. use datalinkage.py to perform fuzzymatcher to match the entity with their records
![image](https://user-images.githubusercontent.com/61874750/202962561-9c49af52-8aa8-4d08-bca1-dfdd33c65ae1.png)
  4.1 also checks for data that matches but not the entity stated in fuzzy
  ![image](https://user-images.githubusercontent.com/61874750/202963381-3258da1a-419c-482e-83cf-2537f8572dfb.png)

5. Startup Elasticsearch
1. Edit elasticsearch.yml in config folder with
![image](https://user-images.githubusercontent.com/61874750/202965280-b4c53ffb-4bba-41e1-a103-b55fc2005c13.png)

6. run elasticsearch.bat in command prompt
![image](https://user-images.githubusercontent.com/61874750/202965178-d8f902bd-b2a7-4699-8624-1b5a9ca778fd.png)
Get the password
![image](https://user-images.githubusercontent.com/61874750/202970855-89c949a6-d69f-4efa-b807-53edc6ba3a2d.png)

7. Make sure is connected to Elasticsearch
  localhost:9200
8.![image](https://user-images.githubusercontent.com/61874750/202973580-b41e274d-3777-449a-b16d-3550a151d0f9.png)
  ![image](https://user-images.githubusercontent.com/61874750/202973537-221c31d4-3d9a-4a80-8047-95ead747600c.png)

9. Reset Kibana password
![image](https://user-images.githubusercontent.com/61874750/202991290-c494adc7-4fae-4423-9d8d-e1dc3a4a53a3.png)
![image](https://user-images.githubusercontent.com/61874750/202991387-724826fd-55a2-41cc-9e99-161456f160ef.png)
