import requests
import json
import csv

# Solicita o ID_NFT do NFT no xDraco ex: https://xdraco.com/nft/trade/12345 (12345)
id_nft = input("Por favor, insira o ID_NFT: ")

# Define se deve incluir pedras que começam com "[E] Magic Stone"
include_e_stones = True  # Altere para False se não quiser incluir

# URL da API para obter o transportID
summary_url = f"https://webapi.mir4global.com/nft/character/summary?seq={id_nft}&languageCode=en"

# Faz a requisição à API para obter o transportID
summary_response = requests.get(summary_url)

# Verifica se a requisição foi bem-sucedida
if summary_response.status_code == 200:
    try:
        summary_data = summary_response.json()  # Converte a resposta da API em um dicionário Python
        print("Dados recebidos da API de resumo:")
        print(json.dumps(summary_data, indent=4))  # Imprime o JSON retornado de forma legível
        
        # Verifica se a chave 'data' está presente no JSON retornado
        if 'data' in summary_data and 'character' in summary_data['data']:
            transport_id = summary_data['data']['character']['transportID']
            print(f"TransportID obtido: {transport_id}")
            
            # URL da API com o transportID obtido
            inven_url = f"https://webapi.mir4global.com/nft/character/inven?transportID={transport_id}&languageCode=en"
            
            # Faz a requisição à API para obter os itens
            inven_response = requests.get(inven_url)
            
            # Verifica se a requisição foi bem-sucedida
            if inven_response.status_code == 200:
                data = inven_response.json()  # Converte a resposta da API em um dicionário Python
                print("Dados recebidos da API de inventário:")
                print(json.dumps(data, indent=4))  # Imprime o JSON retornado de forma legível
                
                # Verifica se a chave 'data' está presente no JSON retornado
                if 'data' in data:
                    items = data['data']  # A lista de itens está na chave 'data'
                    print(f"Número de itens recebidos: {len(items)}")
                    
                    # Filtra itens cujo itemName começa com "[L] Magic Stone" ou "[E] Magic Stone" se a opção estiver ativada
                    filtered_items = [
                        {"itemName": item.get("itemName", "N/A"), "itemUID": item.get("itemUID", "N/A")}
                        for item in items
                        if item.get("itemName", "").startswith("[L] Magic Stone") or (include_e_stones and item.get("itemName", "").startswith("[E] Magic Stone"))
                    ]
                    
                    print(f"Número de itens filtrados: {len(filtered_items)}")
                    print("Itens filtrados:")
                    print(json.dumps(filtered_items, indent=4))

                    # Lista para armazenar os detalhes dos itens
                    item_details = []

                    # URL base da API para obter os detalhes dos itens
                    base_url = "https://webapi.mir4global.com/nft/character/itemdetail"

                    # Itera sobre cada item filtrado e faz a requisição para obter os detalhes
                    for item in filtered_items:
                        itemUID = item["itemUID"]
                        
                        # Monta a URL da API com os parâmetros necessários
                        detail_url = f"{base_url}?transportID={transport_id}&class=1&itemUID={itemUID}&languageCode=en"
                        
                        # Faz a requisição à API para obter os detalhes do item
                        response = requests.get(detail_url)
                        
                        # Verifica se a requisição foi bem-sucedida
                        if response.status_code == 200:
                            item_detail = response.json()  # Converte a resposta da API em um dicionário Python
                            
                            # Extrai as informações necessárias
                            item_info = {
                                "itemName": item_detail["data"]["itemName"],
                                "options": []
                            }
                            
                            # Função para calcular o valor final
                            def calculate_final_value(option_value, trance_step, trance_value, format):
                                final_value = option_value + (trance_step or 0) + trance_value
                                if format == "%":
                                    return f'{round(final_value, 2)}%'
                                return round(final_value, 2)

                            # Dicionário para armazenar opções somadas
                            option_sums = {}

                            # Adiciona as opções principais
                            for option in item_detail["data"]["options"]:
                                option_name = option["optionName"]
                                option_value = calculate_final_value(option["optionValue"], option.get("tranceValue"), 0, option["optionFormat"])
                                if option_name in option_sums:
                                    option_sums[option_name] += option_value
                                else:
                                    option_sums[option_name] = option_value
                            
                            # Adiciona as opções adicionais
                            for add_option in item_detail["data"]["addOptions"]:
                                option_name = add_option["optionName"]
                                option_value = calculate_final_value(add_option["optionValue"], add_option.get("optionTranceStep"), add_option.get("tranceValue", 0), add_option["optionAddFormat"])
                                if option_name in option_sums:
                                    option_sums[option_name] += option_value
                                else:
                                    option_sums[option_name] = option_value
                            
                            # Adiciona as opções somadas ao item_info
                            for option_name, option_value in option_sums.items():
                                item_info["options"].append({
                                    "optionName": option_name,
                                    "optionValue": option_value
                                })
                            
                            item_details.append(item_info)  # Adiciona os detalhes do item à lista
                        else:
                            print(f"Falha ao acessar a API para itemUID {itemUID}. Status code: {response.status_code}")

                    # Salva os detalhes dos itens em um novo arquivo JSON
                    output_filename = f"legendary_stones_{id_nft}.json"
                    with open(output_filename, "w") as json_file:
                        json.dump(item_details, json_file, indent=4)

                    print(f"Detalhes dos itens salvos em '{output_filename}'.")

                    # Coleta todos os nomes de opções únicos
                    all_option_names = set()
                    for item in item_details:
                        for option in item["options"]:
                            all_option_names.add(option["optionName"])

                    # Exporta os detalhes dos itens para um arquivo CSV
                    csv_filename = f"legendary_stones_{id_nft}.csv"
                    with open(csv_filename, "w", newline='') as csv_file:
                        csv_writer = csv.writer(csv_file)
                        
                        # Escreve o cabeçalho
                        headers = ["Stone Name"] + list(all_option_names)
                        csv_writer.writerow(headers)
                        
                        # Escreve os dados
                        for item in item_details:
                            row = [item["itemName"]]
                            option_dict = {option["optionName"]: option["optionValue"] for option in item["options"]}
                            row.extend(option_dict.get(option_name, "") for option_name in all_option_names)
                            csv_writer.writerow(row)

                    print(f"Detalhes dos itens exportados para '{csv_filename}'.")
                else:
                    print("A chave 'data' não foi encontrada na resposta da API de inventário.")
            else:
                print(f"Falha ao acessar a API de inventário. Status code: {inven_response.status_code}")
        else:
            print("A chave 'data' ou 'character' não foi encontrada na resposta da API de resumo.")
    except json.JSONDecodeError:
        print("Erro ao decodificar o JSON. A resposta da API pode estar malformada.")
else:
    print(f"Falha ao acessar a API de resumo. Status code: {summary_response.status_code}")
