import click
import six
import pprint


@click.group()
def cli():
    pass

@cli.command()
@click.argument('folder_name')
@click.option('--debug', default=False)
@click.option('--skip_folders', default='', help="""subfolders not to read, given as the name of a single folder, or a string with names of more folders seperated by ', '""")
def folder2db(folder_name, debug, skip_folders):
    import os
    import folder2db

    skip = []
    for s in skip_folders.split(', '):
        for sk in s.split(','):
            skip.append(sk)
    folder2db.main(folder_name, debug, skip)


@cli.command()
@click.argument('dbfile')
@click.option('--start_id', default=1, type=int)
@click.option('--write_reaction', default=True, type=bool)
@click.option('--write_reaction_system', default=True, type=bool)
@click.option('--write_ase', default=True, type=bool)
@click.option('--write_publication', default=True, type=bool)
def db2server(dbfile, start_id, write_reaction, write_ase, write_publication,
              write_reaction_system):
    import os
    import db2server
    db2server.main(dbfile, start_id=start_id, write_reaction=write_reaction,
                   write_ase=write_ase,
                   write_publication=write_publication,
                   write_reaction_system=write_reaction_system)



@cli.command()
@click.argument('template')
@click.option('--create-template', is_flag=True, help="Create an empty template file.")
@click.option('--custom-base', )
def make_folders(create_template, template, custom_base, ):
    """Create a basic folder tree to put in DFT calculcations.

    Dear all

    Use this command make the right structure for your folders
    for submitting data for Catalysis Hub.
    
    Start by creating a template file by calling:
    
    $ cathub make_folders --create-template <template_name>

    Then open the template and modify it to so that it contains the information
    for you data. You will need to enter publication/dataset information,
    and specify the types of surfaces, facets and reactions. 

    The 'reactions' key is a list of dictionaries. 
    A new dictionary is required for each reaction, and should include two 
    lists, 'reactants' and 'products'. Remember to balance the equation and 
    include a minus sign in the name when relevant.

    'reactions': [
        {
          'reactants': ['CCH3star@ontop'], 
          'products': ['Cstar@hollow', 'CH3star@ontop']
        },
        {
           'reactants': ['CH4gas', '-0.5H2gas', 'star'],
           'products':  ['CH3star']
        }
     ]

    Also, include the phase and of the species as an extension:
      'gas' for gas phase (i.e. CH3 -> CH3gas)
      'star' for empty site or adsorbed phase. (i.e. OH -> OHstar)

    The site of adsorbed species is also included as an extension:
      '@site' (i.e. OHstar in bridge-> OHstar@bridge)

    Then, save the template and call:
    
    $ cathub make_folders <template_name>

    And folders will be created automatically. 

    You can create several templates and call make_folders again
    if you, for example, are using different functionals or are 
    doing different reactions on different surfaces.
    """
    import make_folders_template
    import json
    import os

    if custom_base is None:
        custom_base = os.path.abspath(os.path.curdir)

    template_data = {
        'title': 'Fancy title',
        'authors': ['Doe, John', 'Einstein, Albert'],
        'journal': 'JACS',
        'volume': '1',
        'number': '1',
        'pages': '23-42',
        'year': '2017',
        'publisher': 'ACS',
        'doi': '10.NNNN/....',
        'DFT_code': 'Quantum Espresso',
        'DFT_functional': 'BEEF-vdW',
        'reactions': [
                {'reactants': ['2.0H2Ogas', '-1.5H2gas', 'star'], 
                 'products': [ 'OOHstar@top']},
                {'reactants': ['CCH3star@bridge'], 'products': ['Cstar@hollow', 'CH3star@ontop']},
                {'reactants': ['CH3gas', 'star'], 'products': ['CH3star@ontop']}
        ],
        'surfaces': ['Pt'],
        'facets': ['111']
    }
    if template is not None:
        if create_template:
            if os.path.exists(template):
                raise UserWarning(
                    "File {template} already exists. Refusing to overwrite".format(**locals()))
            with open(template, 'w') as outfile:
                outfile.write(json.dumps(template_data, indent=4,
                                         separators=(',', ': '), sort_keys=True) + '\n')
                return
        else:
            with open(template) as infile:
                template_data = json.load(infile)
                title = template_data['title']
                authors = template_data['authors']
                journal = template_data['journal']
                volume = template_data['volume']
                number = template_data['number']
                pages = template_data['pages']
                year = template_data['year']
                publisher = template_data['publisher']
                doi = template_data['doi']
                dft_code = template_data['DFT_code']
                dft_functional = template_data['DFT_functional']
                reactions = template_data['reactions']
                surfaces = template_data['surfaces']
                facets = template_data['facets']

    make_folders_template.main(
        title=title,
        authors=eval(authors) if isinstance(
            authors, six.string_types) else authors,
        journal=journal,
        volume=volume,
        number=number,
        pages=pages,
        year=year,
        publisher=publisher,
        doi=doi,
        DFT_code=dft_code,
        DFT_functional=dft_functional,
        reactions=eval(reactions) if isinstance(
            reactions, six.string_types) else reactions,
        custom_base=custom_base,
        surfaces=surfaces,
        facets=facets
    )


@cli.command()
def psql_server_connect():
    """Test connection to PostreSQL server."""
    import psql_server_connect


@cli.command()
@click.argument('user')
@click.argument('pub_level')
@click.argument('DFT_level')
@click.argument('XC_level')
@click.argument('reaction_level')
@click.argument('metal_level')
@click.argument('facet_level')
@click.argument('site_level')
@click.argument('final_level')
def write_user_spec():
    """Write JSON specfile for single DFT calculation."""
    import write_user_spec
