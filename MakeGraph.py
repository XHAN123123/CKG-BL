import os
import csv
import javalang
import re

def extract_relationships(source_folder, output_csv):
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

                                    # 处理包与类之间的haveclass关系
                                    writer.writerow([package_name, 'haveclass', full_class_name])

                                    # 处理类与类之间的继承关系
                                    if node.extends:
                                        extends_class = node.extends.name
                                        writer.writerow([full_class_name, 'extends', extends_class])

                                    for member in node.body:
                                        if isinstance(member, javalang.tree.MethodDeclaration):
                                            method_name = member.name
                                            full_method_name = full_class_name + '.' + method_name

                                            # 处理类与方法之间的hasMethod关系
                                            writer.writerow([full_class_name, 'hasMethod', full_method_name])

                                            # 处理方法与参数之间的hasParameter关系
                                            for parameter in member.parameters:
                                                parameter_name = parameter.name
                                                full_parameter_name = full_method_name + '.' + parameter_name
                                                writer.writerow([full_method_name, 'hasParameter', full_parameter_name])

                                            # 处理方法与变量之间的hasVariable关系
                                                # 处理方法与变量之间的 havevariable 关系
                                            if member.body:
                                                for stmt in member.body:
                                                    if isinstance(stmt, javalang.tree.LocalVariableDeclaration):
                                                        for variable in stmt.declarators:
                                                            variable_name = variable.name
                                                            full_variable_name = full_method_name + '.' + variable_name
                                                            writer.writerow([full_method_name, 'havevariable',
                                                                                 full_variable_name])

                                                        # 处理方法参数与变量之间的 havevariable 关系
                                                        for parameter in member.parameters:
                                                            parameter_name = parameter.name
                                                            full_parameter_name = full_method_name + '.' + parameter_name
                                                            writer.writerow([full_method_name, 'havevariable',
                                                                                full_parameter_name])

                                            # 处理方法的注释
                                            if member.documentation:
                                                comment = member.documentation.strip()
                                                writer.writerow([full_method_name, 'hasComment', comment])

                                            # 处理方法与方法之间的调用关系
                                            for call in member.filter(javalang.tree.MethodInvocation):
                                                for argument in call:
                                                    if isinstance(argument, javalang.tree.MethodInvocation):
                                                        call_method = argument.member
                                                        if isinstance(call_method, javalang.tree.MemberReference):
                                                            call_method = call_method.member
                                                        full_call_method = full_class_name + '.' + call_method
                                                        writer.writerow([full_method_name, 'calls', full_call_method])
                        except javalang.tokenizer.LexerError as e:
                            if 'Unterminated block comment' in str(e):
                                print(f'Warning:skipping annlysis of comments in file:{filepath}')
                                continue
                            else:
                                print(f"warning skipping analysis of code: {filepath}")
                                continue
                        except RecursionError as e:
                            print(f"skipping {filepath}")
                            continue
                        except javalang.parser.JavaSyntaxError:
                        # 使用正则表达式提取类名、方法名、参数名、变量名和方法注释
                            with open(filepath, 'r', encoding='utf-8') as fallback_file:
                                content = fallback_file.read()
                                class_names = re.findall(r'class\s+([a-zA-Z_$][a-zA-Z\d_$]*)', content)
                                method_names = re.findall(r'\b[a-zA-Z_$][a-zA-Z\d_$]*\s+([a-zA-Z_$][a-zA-Z\d_$]*)\s*\(',content)
                                variable_names = re.findall(r'\b[a-zA-Z_$][a-zA-Z\d_$]*\s+([a-zA-Z_$][a-zA-Z\d_$]*)\s*;',content)
                                parameter_names = re.findall(r'\((.*?)\)', content)
                                method_comments = re.findall(r'/\*\*(.*?)\*\*/', content,re.DOTALL)

                                for class_name in class_names:
                                    writer.writerow([package_name, 'haveclass', class_name])

                                for method_name in method_names:
                                    full_method_name = package_name + '.' + method_name if package_name else method_name
                                    writer.writerow([package_name, 'hasmethod', full_method_name])

                                for variable_name in variable_names:
                                    full_variable_name = package_name + '.' + variable_name if package_name else variable_name
                                    writer.writerow([package_name, 'hasVariable', full_variable_name])

                                for parameter_name in parameter_names:
                                    parameter_name = parameter_name.strip()
                                    if parameter_name:
                                        full_parameter_name = package_name + '.' + parameter_name if package_name else parameter_name
                                        writer.writerow([full_method_name, 'hasParameter',full_parameter_name])

                                for method_comment in method_comments:
                                    writer.writerow([full_method_name, 'hasComment', method_comment])

                        except UnicodeDecodeError:
                            print(f'UnicodeDecodeError Parsing error in file: {filepath}')
                            continue
    print(f'Code analysis completed. Results are stored in {output_csv}')


# 输入源代码文件夹路径和输出CSV文件路径
source_folder = 'G:\KGBL_Code\dataset\EclipseUI'
output_csv = 'G:\KGBL_Code\graph_CSV\EclipseUI.csv'

# 提取关系并输出到CSV文件
extract_relationships(source_folder, output_csv)