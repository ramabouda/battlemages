export class MultiplexedConsumer {
  constructor (stream) {
    this.stream = stream
    this.multiplexer = null   // Defined by the multiplexer class when added
  }

  connect () {

  }

  disconnect () {

  }

  receive (message) {

  }

  // message needs to be a JSON serializable object
  send (message) {
    if (!this.multiplexer) throw new Error('A multiplexed consumer needs a demultiplexer.')
    this.multiplexer.multiplex(this.stream, message)
  }
}


export class MultiplexedWebsocket {
  constructor (websocket) {
    this.messageIndex = 0
    this.consumers = {} // Consumers indexed by stream

    this.ws = websocket
    this.ws.onopen = this.connect.bind(this)
    this.ws.onclose = this.disconnect.bind(this)

    this.ws.onmessage = this.demultiplex.bind(this)
  }

  addConsumer (consumer) {
    this.consumers[consumer.stream] = consumer
    consumer.multiplexer = this
  }

  demultiplex (response) {
    const message = JSON.parse(response.data)
    if (!message.stream) {
      throw new Error('This message has no stream field : ' + message)
    }
    if (this.consumers[message.stream]) {
      this.consumers[message.stream].receive(message.payload)
    }
  }

  multiplex (stream, message) {
    this.messageIndex += 1
    this.ws.send(JSON.stringify({
      order: this.messageIndex, // required to have ordered messages
      stream: stream,
      payload: message,
    }))
  }

  connect () {
    Object.keys(this.consumers).forEach(k => this.consumers[k].connect())
  }

  disconnect () {
    Object.keys(this.consumers).forEach(k => this.consumers[k].disconnect())
  }
}
