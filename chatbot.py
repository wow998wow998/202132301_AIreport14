import pandas as pd
#레벤슈타인 거리를 이용하여 챗봇을 만들때는 별도의 함수를 사용하지 않고 거리를 계산


 # 챗봇 객체를 초기화하는 메서드, 초기화 시에는 입력된 데이터 파일을 로드
class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)
        #질문을 Tf-Idf로 변환하지 않았기 때문에 삭제함

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers
    
    # 가장 좋은 답을 찾는 함수를 정의합니다.
    def find_best_answer(self, input_sentence):
        min_distance = float('inf') #최소 거리를 무한대로 설정함
        best_answer = None #최적의 답변은 None으로 설정함
        for i, question in enumerate(self.questions): #enumerate함수를 이용해 인덱스와 질문열 값을 가져옴
            distance = self.calc_distance(input_sentence, question)
            
            #입력한 문장과 질문열간의 레비슈타인거리를 미리 정의한 함수를 이용하여 구함.
            if distance < min_distance: #계산한 거리 중 최소 거리를 찾는 반복문.
                min_distance = distance
                best_answer = self.answers[i]#최소 거리를 갖는 답변을 반환
        return best_answer


    #레벤슈타인 거리 계산하는 함수
    def calc_distance(self, a, b):
    
        if a == b: return 0 # 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이

        if a == "": # a 가 아무것도 입력되어있지 않다면 b문자열의 길이를 반환
            return b_len
        
        if b == "": # b 가 아무것도 입력되어있지 않다면 a문자열의 길이를 반환
            return a_len
        
        matrix = [[0 for j in range(b_len + 1)] for i in range(a_len + 1)]
        #리스트 컴프리헨션을 이용해 2차원 리스트를 초기화
        #i 와 j 변수가 너무 많이 쓰여 리스트 생성 코드를 간략화 함

        #matrix열의 첫번째 열을 a_len부터 0까지 순서대로 입력
        for i in range(a_len + 1):
            matrix[i][0] = i
                
        #matrix행의 첫번째 행을 B_len부터 0까지 순서대로 입력
        for j in range(b_len + 1):
            matrix[0][j] = j

        #matrix의 첫번째 행과 첫번째 열을 제외한 나머지 부분을 채우기 위한 반복문
        for i in range(1, a_len+1):
            ac = a[i-1]
            for j in range(1, b_len+1):
                bc = b[j-1] 

                #본격적으로 거리를 구해가는 과정
                cost = 0 if (ac == bc) else 1 # 비교하는 글자가 같으면 0, 다르면 1
                matrix[i][j] = min([
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                ])
            
        return matrix[a_len][b_len] # 최종 계산된 거리값을 반환
    
# CSV 파일 경로를 지정하세요.
filepath = 'ChatbotData.csv'

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)



# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
    
