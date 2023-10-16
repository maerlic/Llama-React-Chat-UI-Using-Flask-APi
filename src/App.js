import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [messages, setMessages] = useState([]);
    const [response, setResponse] = useState("");
    const serverURL = `http://127.0.0.1:5000/`;

    const handleChange = (e) => {
        setInput(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        const instance = axios.create({
        baseURL: serverURL,
        withCredentials: false,
        headers: {
            "Content-Type": "application/json",
        },
        });

        try {
        const requestBody = {
            messages: [
            {
                role: "user",
                content: input,
            },
            ],
        };

        const response = await instance.post("/chat", requestBody);
        setResponse(response.data.choices[0].message.content);
        } catch (error) {
        console.error("Error sending message:", error);
        } finally {
        setLoading(false);
        }
    };

    return (
        <div className="container">
        <header className="header">
            <h1>Marco's Llama 2 ChatBot</h1>
        </header>
        <main>
            <form onSubmit={handleSubmit}>
            <div className="form-group">
                <label htmlFor="input">Your question:</label>
                <input
                id="input"
                type="text"
                className="form-control"
                value={input}
                onChange={handleChange}
                />
            </div>
            <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "Loading..." : "Submit"}
            </button>
            </form>
            <MessageList messages={messages} response={response} />
        </main>
        </div>
    );
}

function MessageList({ messages, response }) {
    return (
      <div className="message-list">
        <h2>Message History</h2>
        <ul>
          {messages.map((message, index) => (
            <li key={index}>
              <strong>{message.role === "user" ? "User" : "ChatGPT"}:</strong>{" "}
              {message.content.includes("") ? (
                <pre
                  className={message.role === "user" ? "user-code" : "chatgpt-code"}
                >
                  <code>{message.content.replace(/ /g, "")}</code>
                </pre>
              ) : (
                <pre
                  className={
                    message.role === "user" ? "user-message" : "chatgpt-message"
                  }
                >
                  {message.content}
                </pre>
              )}
            </li>
          ))}
          {response && (
            <li>
              <strong>ChatGPT Response:</strong>{" "}
              <pre className="chatgpt-message">{response}</pre>
            </li>
          )}
        </ul>
      </div>
    );
  }

export default App;
