from subprocess import check_call

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz

iris = load_iris()
x = iris.data[:, 2:]
y = iris.target

tree_model = DecisionTreeClassifier(max_depth=3)
tree_model.fit(x, y)

export_graphviz(
    tree_model,  # 학습한 모형
    out_file='./iris_tree_model.dot',  # .dot 파일 저장 위치
    feature_names=iris.feature_names[2:],  # 사용한 변수 이름
    class_names=iris.target_names,  # 예측할 타겟 클래스 이름
    rounded=True,  # 사각형 끝을 둥글게
    filled=True  # 사각형 안 색깔 채우기
)
# 예측한 모형 png로 바꿔서, 시각화 하기
check_call(['dot', '-Tpng', 'iris_tree_model.dot', '-o', 'OutputFile.png'])
