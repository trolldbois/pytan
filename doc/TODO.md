TODO:
 - port check pre auth
 - auth with U/P, get session token & use that, get server version and debug print
 - if session token expired, re-auth with U/P
 - override WSDL with local file
    def ask_question(self, question):
        '''
        create_soap_message
        get_parsed_question_results
        maybe debug print the full parsed question list, but just pick the first for now
        run the question
        get result info over and over again until questions is "finished"
        build result set from final result info
        convert result set to format (i.e csv)
        return format
        '''
