#include "morse.h"

int main()
{
    MorseNode *morse_sequence_head = NULL, *morse_sequence_tail = NULL;

    gpio_t *dot = NULL;
    gpio_t *dash = NULL;
    gpio_t *accept = NULL;
    gpio_t *diode = NULL;
    
    fprintf(stderr,"Preparing DIODE...\n");
    open_diode(&diode);

    /* Diode Tests */

    // push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
    // push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
    // push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
    // MorseNode *iterator = morse_sequence_head;
    // display_morse_sequence(diode, iterator);
    // clear_sequence(&morse_sequence_head, &morse_sequence_tail);
    // push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
    // push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
    // push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
    // iterator = morse_sequence_head;
    // display_morse_sequence(diode, iterator);
    // clear_sequence(&morse_sequence_head, &morse_sequence_tail);

    fprintf(stderr,"Preparing DOT button...\n");
    open_button(&dot, BUTTON_DOT_PIN, BUTTON_PATH);
    fprintf(stderr,"Preparing DASH button...\n");
    open_button(&dash, BUTTON_DASH_PIN, BUTTON_PATH);
    fprintf(stderr,"Preparing ACCEPT button...\n");
    open_button(&accept, BUTTON_ACCEPT_PIN, BUTTON_PATH);
    
    gpio_t *buttons[] = { dot, dash, accept };
    uint64_t timestamps[] = {0ULL, 0ULL, 0ULL};
    bool ready[] = { false, false, false };
    
    size_t buttons_count = sizeof(buttons) / sizeof(gpio_t *);

    while(true){
        int ready_count = 0;

        fprintf(stderr,"Waiting for the buttons to be pressed...\n");

        ready_count = gpio_poll_multiple(
            buttons, 
            buttons_count, 
            MULTIPLE_POOL_TIMEOUT, 
            ready
        );
        
        if(ready_count < 0){
            fprintf(stderr, "gpio_poll_multiple(): error code %d\n", ready_count);
            exit(EXIT_FAILURE);
        }
        else if (ready_count == 0) {
            fprintf(stderr,"Timeout has occurred, no morse signals detected, finishing execution...\n");
            goto cleanup;
        }
        
        fprintf(stderr,"A button event has occurred...\n");
        
        gpio_edge_t edge;
        uint64_t timestamp;

        /* DOT */
        if(ready[BUTTON_DOT_INDEX]){
            if (gpio_read_event(buttons[BUTTON_DOT_INDEX], &edge, &timestamp) < 0) {
                fprintf(stderr, "gpio_read_event(): %s\n", gpio_errmsg(buttons[BUTTON_DOT_INDEX]));
                goto cleanup;
            }

            if(has_miliseconds_passed(timestamps[BUTTON_DOT_INDEX], timestamp, DEBOUNCE_DELAY_MILISECONDS)){
                fprintf(stderr, "DOT clicked.\n");
                push_back_signal(&morse_sequence_head, &morse_sequence_tail, DOT);
            }
            else {
                fprintf(stderr, "DOT bounce.\n");
            }

            timestamps[BUTTON_DOT_INDEX] = timestamp;
            ready[BUTTON_DOT_INDEX] = false;
        }

        /* DASH */
        if(ready[BUTTON_DASH_INDEX]){
            if (gpio_read_event(buttons[BUTTON_DASH_INDEX], &edge, &timestamp) < 0) {
                fprintf(stderr, "gpio_read_event(): %s\n", gpio_errmsg(buttons[BUTTON_DASH_INDEX]));
                goto cleanup;
            }

            if(has_miliseconds_passed(timestamps[BUTTON_DASH_INDEX], timestamp, DEBOUNCE_DELAY_MILISECONDS)){
                fprintf(stderr, "DASH clicked.\n");
                push_back_signal(&morse_sequence_head, &morse_sequence_tail, DASH);
            }
            else {
                fprintf(stderr, "DASH bounce.\n");
            }

            timestamps[BUTTON_DASH_INDEX] = timestamp;
            ready[BUTTON_DASH_INDEX] = false;
        }

        /* ACCEPT */
        if(ready[BUTTON_ACCEPT_INDEX]){
            if (gpio_read_event(buttons[BUTTON_ACCEPT_INDEX], &edge, &timestamp) < 0) {
                fprintf(stderr, "gpio_read_event(): %s\n", gpio_errmsg(buttons[BUTTON_ACCEPT_INDEX]));
                goto cleanup;
            }

            if(has_miliseconds_passed(timestamps[BUTTON_ACCEPT_INDEX], timestamp, DEBOUNCE_DELAY_MILISECONDS)){
                fprintf(stderr, "ACCEPT clicked.\n");
                
                if(morse_sequence_head == NULL){
                    printf("Stop conditions satisfied, finishing execution...\n");
                    goto cleanup;
                }

                MorseNode *iterator = morse_sequence_head;
                display_morse_sequence(diode, iterator);
                clear_sequence(&morse_sequence_head, &morse_sequence_tail);
            }
            else {
                fprintf(stderr, "ACCEPT bounce.\n");
            }

            timestamps[BUTTON_ACCEPT_INDEX] = timestamp;
            ready[BUTTON_ACCEPT_INDEX] = false;
        }
    }
cleanup:
    close_free_button(&dot);
    close_free_button(&dash);
    close_free_button(&accept);

    close_free_button(&diode);

    clear_sequence(&morse_sequence_head, &morse_sequence_tail);

    return EXIT_SUCCESS;
}