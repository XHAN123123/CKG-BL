from py2neo import Graph, Node, Relationship
import csv

# 连接到Neo4j数据库
graph = Graph("http://localhost:7474/", auth=("neo4j", "zzw991115zzw"))

# 定义关系与实体类别的映射关系及颜色
relationship_mapping = {
    "haveclass": ("Package", "Class", "yellow"),
    "extends": ("Class", "Class", "red"),
    "hasMethod": ("Class", "Method", "blue"),
    "hasParameter": ("Method", "Parameter", "green"),
    "methodCall": ("Method", "Method", "orange"),
    "hasComment": ("Method", "Comment", "purple"),
    "hasVariable": ("Method", "Variable", "pink")
}

# 用于存储已创建的实体节点
entity_nodes = {}

# 读取CSV文件
with open('H:\KGBL_Code\graph_CSV\EclipseUI.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        try:
            # 提取数据
            entity1_name = row[0]
            relationship_type = row[1]
            entity2_name = row[2]

            # 根据关系类型获取实体类别和颜色
            entity1_type, entity2_type, color = relationship_mapping.get(relationship_type, ("", "", ""))

            # 创建或获取实体1节点
            if entity1_name in entity_nodes:
                entity1_node = entity_nodes[entity1_name]
            else:
                entity1_node = Node(entity1_type, name=entity1_name)
                entity1_node["color"] = color
                entity_nodes[entity1_name] = entity1_node
                graph.create(entity1_node)

        # 创建或获取实体2节点
            if entity2_name in entity_nodes:
                entity2_node = entity_nodes[entity2_name]
            else:
                entity2_node = Node(entity2_type, name=entity2_name)
                entity2_node["color"] = color
                entity_nodes[entity2_name] = entity2_node
                graph.create(entity2_node)

        # 创建关系
            relationship = Relationship(entity1_node, relationship_type, entity2_node)
            graph.create(relationship)

        except Exception as e:
            print("Error processiong triple:",row)



