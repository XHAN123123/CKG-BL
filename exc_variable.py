import os
import csv
import javalang

def extract_variable_relationships(source_folder, output_csv):
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Subject', 'Relation', 'Object'])

        for (dirpath, dirnames, filenames) in os.walk(source_folder):
            for filename in filenames:
                if filename.endswith('.java'):
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        try:
                            tree = javalang.parse.parse(file.read())

                            # 提取包名
                            package_name = tree.package.name if tree.package else ''

                            for path, node in tree:
                                if isinstance(node, javalang.tree.PackageDeclaration):
                                    package_name = node.name

                                if isinstance(node, javalang.tree.ClassDeclaration):
                                    class_name = node.name
                                    full_class_name = package_name + '.' + class_name if package_name else class_name

                                    for member in node.body:
                                        if isinstance(member, javalang.tree.MethodDeclaration):
                                            method_name = member.name
                                            full_method_name = full_class_name + '.' + method_name

                                            # 处理方法与变量之间的 havevariable 关系
                                            if member.body:
                                                for stmt in member.body:
                                                    if isinstance(stmt, javalang.tree.LocalVariableDeclaration):
                                                        for variable in stmt.declarators:
                                                            variable_name = variable.name
                                                            full_variable_name = full_method_name + '.' + variable_name
                                                            writer.writerow([full_method_name, 'havevariable', full_variable_name])

                                                        # 处理方法参数与变量之间的 havevariable 关系
                                                        for parameter in member.parameters:
                                                            parameter_name = parameter.name
                                                            full_parameter_name = full_method_name + '.' + parameter_name
                                                            writer.writerow([full_method_name, 'havevariable', full_parameter_name])
                        except javalang.parser.JavaSyntaxError:
                            print(f'Parsing error in file: {filepath}')

    print(f'Variable relationship extraction completed. Results are stored in {output_csv}')


# 输入源代码文件夹路径和输出CSV文件路径
source_folder = 'G:/KGBL_Code/dataset/SWT-3.1'
output_csv = 'G:/KGBL_Code/graph_CSV/SWT_variable.csv'

# 提取方法与变量之间的关系并输出到CSV文件
extract_variable_relationships(source_folder, output_csv)