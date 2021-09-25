using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WebSocketClientTest : MonoBehaviour
{
    public Connection c;
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
    public void onClickSendMsg()
    {
        c.SendMessage("Msg");
    }
}
