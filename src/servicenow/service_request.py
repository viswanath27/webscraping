from pysnc import ServiceNowClient, ServiceNowOAuth2
password ="Bvyssu_27"
client = ServiceNowClient('http://www.service-now.com', ('admin',password))
#client = ServiceNowClient('dev0000', ServiceNowOAuth2('integration.user', password))
print ("Done with Authentication ")
# gr = client.GlideRecord('sys_user')
# print("Done with client creation")
# gr.add_query('user_name', 'admin')
# print("getting the query results")
# gr.query()

def get_request_details():
    pass

def update_request(id, new_value):
    gr = client.GlideRecord('problem')
    gr.get(id)
    gr.short_description = new_value
    id = gr.update()
    return id

def get_request_status(id):
    pass

def create_request():
    print("Init the problem class")
    gr = client.GlideRecord('problem')
    print("Init the problem class")
    gr.initialize()
    print("Provide description")
    gr.short_description = "Example Problem"
    gr.description = "Example Description"
    print("insert")
    id = gr.insert()
    print("done with authentication")
    return id 
# for r in gr:
#     print(r.sys_id)

print(create_request())
# gr = client.GlideRecord('incident')
# gr.add_query("active", "true")
# print(gr.query())