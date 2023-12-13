const express = require('express');
const {PubSub} = require('@google-cloud/pubsub');
const path = require('path');

const app = express();
const pubSubClient = new PubSub();

const topicId = 'topic-id';
const subscriptionId = 'sub-id';

app.set('view engine', 'pug');
app.set('views', path.join(__dirname, 'views'));

app.get('/', async (req, res) => {
 const subscription = pubSubClient.subscription(subscriptionId);
 const [messages] = await subscription.pull({maxMessages: 10});
 await subscription.ack(messages.map(message => message.ackId));
 res.render('index', { messages: messages.map(message => message.data.toString()) });
});

app.listen(3000, () => console.log('Server started on port 3000'));