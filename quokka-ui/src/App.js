import React, { Component } from 'react';

class App extends Component {
  state = {
    todos: []
  }
  componentDidMount() {
    fetch('http://127.0.0.1:5000/device?device=devnet-csr-always-on-sandbox&info=arp')
    .then(res => res.json())
    .then((data) => {
      this.setState({ todos: data })
      console.log(this.state.todos)
    })
    .catch(console.log)
  }
  render() {

    return (
//       <div className="container">
//        {JSON.stringify(this.state.todos.arp)}
//        <div className="col-xs-12">
//        <h1>My Todos</h1>
//        {this.state.todos.map((todo) => (
//          <div className="card">
//            <div className="card-body">
//              <h5 className="card-title">{todo.title}</h5>
//              <h6 className="card-subtitle mb-2 text-muted">
//              { todo.completed &&
//                <span>
//                Completed
//                </span>
//              }
//              { !todo.completed &&
//                <span>
//                  Pending
//                </span>
//              }
//              </h6>
//            </div>
//          </div>
//        ))}
//        </div>
//       </div>

       <div className="container">
        <div className="col-xs-12">
        <p>{JSON.stringify(this.state.todos.arp)}</p>
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Example Todo</h5>
              <h6 className="card-subtitle mb-2 text-muted">Completed</h6>
            </div>
          </div>
        </div>
       </div>
    );
  }
 }

export default App;
