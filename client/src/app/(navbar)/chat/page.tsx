"use client"
import React, {ReactNode, useEffect, useState} from 'react';
import "../../styles/globals.css"
import { json } from 'stream/consumers';


interface ChatElem {
  id: number,
  username: string
  content: string
}
const Chat = () => {
  const [inputValue, setInputValue] = useState<string>('');
  const [username, setUsername] = useState<string>('')
  const [ws, setWebSocket] = useState<WebSocket>()
  const [chatData, setChatData] = useState<ChatElem[]>()
  const [chatboxRef, setChatboxRef] = useState<HTMLDivElement | null>(null);

  async function getChat() {
    const response = await fetch("/api/getChat", {
      method: "GET",
    })
    if (response.status == 200) {
        const responseData = await response.json()
        setChatData(responseData)
    }
  }

  const handleKeyPress = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      if (ws) {
        if (inputValue.length != 0) {
          ws.send(JSON.stringify({"type": "postChat", "username": username, "message": inputValue}))
        }
      }
      setInputValue("")
    }
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputValue(event.target.value);
  };

  useEffect(() => {
    if (ws) {
      ws.onopen = () => {
        console.log('WebSocket connected');
      };
    
      ws.onmessage = (event) => {
        console.log('Message received:', event.data);
        getChat()
      };
    
      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    
      ws.onclose = () => {
        console.log('WebSocket closed');
      };
      window.removeEventListener('beforeunload', (() => {
        ws.close();
      }));
    }
  })

  useEffect(() => {
    if (chatboxRef) {
      chatboxRef.scrollTop = chatboxRef.scrollHeight;
    }
    console.log(chatData)
  }, [chatData, chatboxRef]);
  
  async function authenticate() {
    const response = await fetch("/api/authenticate", {
      method: "GET",
    })
    if (response.status == 200) {
        const responseData = await response.json()
        setUsername(responseData['username'])
    }
  }

  useEffect(() => {
    var messageBody = document.querySelector('.chatbox');
    authenticate()
    console.log('ws://' + window.location.host + '/web-socket/chat');
    setWebSocket(new WebSocket('ws://' + window.location.host + '/web-socket/chat'))
    getChat()
    if (messageBody) {
      messageBody.scrollIntoView();
    }
  }, []);


  function serveChat(): ReactNode {
    let chatList = []
    if (chatData) {
      for (let i of chatData) {
        const chatString = i["username"] + ": " + i["content"] 
        chatList.push(<p key={i["id"]}>{chatString}</p>)
      }
    }
    return chatList
  }

  return (
    username !== "" && (
      <div className="homepage">
        <div className="home-section">
          <div className='chatbox' ref={(ref) => setChatboxRef(ref)}>
            {serveChat()}
          </div>
          <input className="chat-input" type='text' value={inputValue} onChange={handleChange} onKeyDown={handleKeyPress} placeholder='Enter message'></input>
        </div>
      </div>
    )
  );
}

export default Chat;