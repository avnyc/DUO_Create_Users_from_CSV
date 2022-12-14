import duo_client
from file_locations import duo_logger, duo_ingestion_file
import pandas as pd
import re
import time

# Make df more reader friendly in 'Run' windows
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False)

# Start timer
start_time = time.time()


class DUO:
    def __init__(self, phone_type, platform, ikey, skey, host):
        try:
            # Import df from HR file
            self.correct = 0
            self.wrong = 0
            self.df = pd.read_csv(filepath_or_buffer=duo_ingestion_file,
                                  delimiter=',',
                                  header=0,
                                  encoding='unicode_escape')
            duo_logger.info(f'Successfully imported DUO CSV file.')
            self.total = self.df.shape[0]

            self.phone_type = phone_type
            self.platform = platform
            self.admin_api = duo_client.Admin(ikey=ikey,
                                              skey=skey,
                                              host=host)
            duo_logger.info(f'Successfully created admin_api object.')
            duo_logger.info(f'-----------------------------------------------------------------------------------')
            duo_logger.info(f'\n')
            self.create_duo_accounts()

        except Exception as e:
            duo_logger.error(f'Failed to  import DUO CSV file. Error is: {e}')

    def create_duo_accounts(self):
        # Iterate over df and create DUO account
        for index, row in enumerate(self.df.itertuples(index=False)):
            try:

                username_ = row.USERNAME
                user_email = row.USER_EMAIL
                full_name = row.FULL_NAME
                phone_number = str(row.PHONE_NUMBER)

                # Count integers in phone_number
                phone_number_length = len(re.sub('[^0-9]', '', phone_number))

                if phone_number_length != 10:
                    duo_logger.error(f'Phone Number is not 10 integers')
                    duo_logger.warning(f"WARNING")
                    duo_logger.warning(f"WARNING")
                    duo_logger.error(f'Please review this data row{row}.')
                    duo_logger.warning(f"WARNING")
                    duo_logger.warning(f"WARNING")
                    duo_logger.info(
                        f'-----------------------------------------------------------------------------------')
                    duo_logger.info(f'\n')

                    # Increment wrong counter
                    self.wrong += 1

                    # Continue Loop
                    continue
                else:
                    duo_logger.info(f'Phone number is the correct number of integers')

                pattern_ = re.compile("^[\dA-Z]{3}-[\dA-Z]{3}-[\dA-Z]{4}$", re.IGNORECASE)
                match_ = pattern_.match(phone_number)

                pattern = re.compile("^[\dA-Z]{3}[\dA-Z]{3}[\dA-Z]{4}$", re.IGNORECASE)
                match = pattern.match(phone_number)

                if match_:
                    duo_logger.info(f'The regex pattern matches this as XXX-XXX-XXXX. This is correct.')
                elif match:
                    duo_logger.info(f'The regex pattern matches this as XXXXXXXXXX. This is correct.')
                else:
                    duo_logger.error(f'The phone number does not match one of the two approved regex patterns. '
                                     f'This phone number is not in the correct format.')

                    duo_logger.warning(f"WARNING")
                    duo_logger.warning(f"WARNING")
                    duo_logger.error(f'Please review this data row{row}.')
                    duo_logger.warning(f"WARNING")
                    duo_logger.warning(f"WARNING")
                    duo_logger.info(
                        f'-----------------------------------------------------------------------------------')
                    duo_logger.info(f'\n')

                    # Increment wrong counter
                    self.wrong += 1

                    # Continue loop to next user
                    continue

                # Create and return a new user object.
                user = self.admin_api.add_user(
                    username=username_,
                    realname=full_name,
                    email=user_email,
                )
                duo_logger.info(f'{username_} was created in DUO.')

                # Create and return a new phone object.
                phone = self.admin_api.add_phone(
                    number=phone_number,
                    type=self.phone_type,
                    platform=self.platform
                )

                # Associate the user with the phone.
                self.admin_api.add_user_phone(
                    user_id=user['user_id'],
                    phone_id=phone['phone_id'],
                )
                duo_logger.info(f"{username_}'s phone was added to DUO.")

                # Send SMS to phone number.
                self.admin_api.send_sms_activation_to_phone(
                    phone_id=phone['phone_id'],
                    install='1',
                )
                # Log text sent and time taken to run script to this point.
                duo_logger.info(f'Successfully sent {username_} a text!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                duo_logger.info(f"Took {((time.time() - start_time) / 60):.3f} minutes to create "
                                f"{username_}'s account.")
                duo_logger.info(f'-----------------------------------------------------------------------------------')
                duo_logger.info(f'\n')

                # Increment correct counter
                self.correct += 1

            except Exception as e:
                duo_logger.error(f"Failed to send {username_}'s {phone_number} a text. Error is {e}.")
                duo_logger.warning(f"WARNING")
                duo_logger.warning(f"WARNING")
                duo_logger.error(f'Please review this data row{row}.')
                duo_logger.warning(f"WARNING")
                duo_logger.warning(f"WARNING")
                duo_logger.info(f'-----------------------------------------------------------------------------------')
                duo_logger.info(f'\n')

                # Increment wrong counter
                self.correct += 1

                # Continue with loop on error
                continue

        # Document how long script took to run
        duo_logger.info(f'\n')
        duo_logger.info(f"Script took {((time.time() - start_time) / 60):.3f} minutes to run in its entirety.")
        duo_logger.info(f'Total correct are: {self.correct}')
        duo_logger.info(f'Total wrong are: {self.wrong}')
        duo_logger.info(f'Total new employees are: {self.total}')
        duo_logger.info(f'Total correct and wrong is {self.correct + self.wrong}')
        if self.total == (self.correct + self.wrong):
            duo_logger.info(f'All lines have been accounted for!')


if __name__ == '__main__':
    # Fill this information in to successfully use DUO Admin API
    DUO(phone_type='',
        platform='',
        ikey='',
        skey='',
        host=''
        )
