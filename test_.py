import json, time
def test_index(app, client):
    myFirstPost = client.post("/push", data={'source_name': 'twins', 'link': 'https://storage.googleapis.com/sieve-public-videos/celebrity-videos/dwyane_basketball.mp4'})
    mySecondPost = client.post("/push", data={'source_name': 'twins', 'link': 'https://storage.googleapis.com/sieve-public-videos/celebrity-videos/elon_podcast.mp4'})
    myFirstList = client.get("/list")
    assert len(eval(myFirstList.get_data(as_text=True))) == 2
    assert myFirstPost.status_code == 200
    assert myFirstList.status_code == 200
    myStatusCheck = client.get(f"/status/{myFirstPost.get_data(as_text=True)}")
    assert myStatusCheck.get_data(as_text=True) == 'queued'
    myStatusCheck = client.get(f"/status/{mySecondPost.get_data(as_text=True)}")
    assert myStatusCheck.get_data(as_text=True) == 'queued'
    time.sleep(5)
    myStatusCheck = client.get(f"/status/{myFirstPost.get_data(as_text=True)}")
    assert myStatusCheck.get_data(as_text=True) == 'processing'
    myStatusCheck = client.get(f"/status/{mySecondPost.get_data(as_text=True)}")
    assert myStatusCheck.get_data(as_text=True) == 'queued'
    time.sleep(10)
    myStatusCheck = client.get(f"/status/{myFirstPost.get_data(as_text=True)}")
    assert myStatusCheck.get_data(as_text=True) == 'finished'
    myStatusCheck = client.get(f"/status/{mySecondPost.get_data(as_text=True)}")
    assert myStatusCheck.get_data(as_text=True) == 'processing'
    time.sleep(10)
    myQueryCheck2 = client.get(f"/query/{myFirstPost.get_data(as_text=True)}")
    print(json.loads(myQueryCheck2.get_data(as_text=True)))
    myQueryCheck = client.get(f"/query/{mySecondPost.get_data(as_text=True)}")
    print(json.loads(myQueryCheck.get_data(as_text=True)))
    assert len(json.loads(myQueryCheck.get_data(as_text=True))['1']['positions']) > 30
    #assert expected == json.loads(res.get_data(as_text=True))