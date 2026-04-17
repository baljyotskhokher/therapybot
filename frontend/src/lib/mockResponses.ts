const responses = [
  "Thank you for sharing that with me. Can you tell me more about how that makes you feel?",
  "I hear you. It sounds like you're going through a lot right now. What do you think would help you feel a little better today?",
  "That's a really important observation. Being aware of your feelings is a great first step.",
  "It's completely okay to feel that way. There's no right or wrong when it comes to emotions.",
  "I appreciate you opening up. What has been on your mind the most lately?",
  "Sometimes just talking about things can bring a sense of relief. I'm here for you.",
  "That takes courage to say. How long have you been feeling this way?",
  "Your feelings are valid. Let's explore that a bit more — what do you think triggered this?",
  "It sounds like you're being really hard on yourself. What would you say to a friend in the same situation?",
  "Take a deep breath. You're doing great just by being here and talking about it.",
];

let index = 0;

export function getMockResponse(): string {
  const response = responses[index % responses.length];
  index++;
  return response;
}
