import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {ChatbotApiClientService} from './services/chatbot-api-client.service';
import {FormsModule} from '@angular/forms';
import {ChatResponse} from './models/chat.models';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, FormsModule],
    templateUrl: './app.component.html',
    standalone: true,
    styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {

    protected chatResponse: ChatResponse = {
        message: "",
        items: undefined,
    };

    protected userChatInput: string = "";
    constructor(private apiClientService: ChatbotApiClientService) {
    }

    public ngOnInit(): void {

    }

    public onKeydown(event: KeyboardEvent) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevents the default action of moving to the next line // Handle the "Enter" key press here console.log('Enter key was pressed.'); } }

            this.apiClientService.getPrograms({
                question: this.userChatInput,
            }).subscribe((programModel) => {
                this.chatResponse = programModel;
            })
        }
    }
}
