import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {ChatbotApiClientService} from './services/chatbot-api-client.service';
import {FormsModule} from '@angular/forms';
import {ChatHistoryMessage, ChatHistoryMessageType, ChatResponse} from './models/chat.models';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, FormsModule],
    templateUrl: './app.component.html',
    standalone: true,
    styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {

    private chatHistoryId = 0;

    protected chatHistoryStack: ChatHistoryMessage[] = [];

    protected userChatInput: string = "какви специалности има?";
    constructor(private apiClientService: ChatbotApiClientService) {
    }

    public ngOnInit(): void {

    }

    public onKeydown(event: KeyboardEvent) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevents the default action of moving to the next line // Handle the "Enter" key press here console.log('Enter key was pressed.'); } }
            this.sendMessage();
        }
    }

    public sendMessage(): void{
        this.chatHistoryStack.push({
            messageType: ChatHistoryMessageType.UserMessage,
            message: this.userChatInput,
            id: this.chatHistoryId++,
            isWarning: false,
        } as ChatHistoryMessage);

        this.apiClientService.getPrograms({
            question: this.userChatInput,
        }).subscribe({ next: (chatResponse) => {

            this.chatHistoryStack.push({
                messageType: ChatHistoryMessageType.BotMessage,
                message: chatResponse.message,
                items: chatResponse.items,
                id: this.chatHistoryId++,
                isWarning: false,
            } as ChatHistoryMessage);
        }, error: (error) =>{
                this.chatHistoryStack.push({
                    messageType: ChatHistoryMessageType.BotMessage,
                    message: error.error.message,
                    id: this.chatHistoryId++,
                    isWarning: true,
                } as ChatHistoryMessage);
        }});

        this.userChatInput = "";
    }

    protected readonly ChatHistoryMessageType = ChatHistoryMessageType;
}
